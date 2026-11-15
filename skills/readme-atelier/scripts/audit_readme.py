#!/usr/bin/env python3
"""Read-only checks for common README references. No network requests or writes."""
from __future__ import annotations

import argparse
from html.parser import HTMLParser
import json
import math
import os
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".avif"}
UNCHECKED = [
    "visual_quality", "command_success", "claim_accuracy", "license_correctness",
    "external_link_availability", "anchor_existence", "gif_playback",
]
INLINE = re.compile(r"(!?)\[([^\]\n]*)\]\(")
REFERENCE = re.compile(r"(!?)\[([^\]\n]*)\]\[([^\]\n]*)\]")
DEFINITION = re.compile(r"(?m)^ {0,3}\[([^\]\n]+)\]:[ \t]*(<[^>\n]*>|[^\s]+)")
SHORTCUT = re.compile(r"(!?)\[([^\]\n]+)\](?![(:\[])")

def without_code(text: str) -> str:
    """Blank code/comments but retain offsets and line numbers."""
    def blank(value):
        return re.sub(r"[^\n]", " ", value)
    lines, fence_char, fence_len = [], None, 0
    for line in text.splitlines(keepends=True):
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line.rstrip("\r\n"))
        if fence_char:
            lines.append(blank(line))
            if marker and marker[1][0] == fence_char and len(marker[1]) >= fence_len and not marker[2].strip():
                fence_char = None
        elif marker:
            fence_char, fence_len = marker[1][0], len(marker[1])
            lines.append(blank(line))
        elif line.startswith(("    ", "\t")):
            lines.append(blank(line))
        else:
            lines.append(line)
    clean = "".join(lines)
    clean = re.sub(r"<!--.*?-->", lambda m: blank(m[0]), clean, flags=re.S)
    return re.sub(r"(`+)([^\n]*?)\1", lambda m: blank(m[0]), clean)

def destination(text: str, start: int) -> str:
    """Read a Markdown destination with angle brackets or balanced parentheses."""
    pos = start
    while pos < len(text) and text[pos].isspace():
        pos += 1
    if pos < len(text) and text[pos] == "<":
        end = text.find(">", pos + 1)
        return text[pos + 1:end] if end >= 0 else ""
    result, depth = [], 0
    while pos < len(text):
        ch = text[pos]
        if ch == "\\" and pos + 1 < len(text) and text[pos + 1] in "()":
            result.append(text[pos + 1])
            pos += 2
            continue
        if ch.isspace() or (ch == ")" and depth == 0):
            break
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        result.append(ch)
        pos += 1
    return "".join(result)

class HTMLReferences(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.items = []

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        line = self.getpos()[0]
        if tag == "img":
            self.items.append((values.get("src", ""), True, values.get("alt", ""), line))
        if tag in {"img", "source"}:
            srcset = values.get("srcset", "")
            # Data-URL commas do not delimit candidates; leave these for manual inspection.
            if not srcset.lstrip().startswith("data:"):
                for candidate in srcset.split(","):
                    if candidate.strip():
                        self.items.append((candidate.strip().split()[0], True, "srcset", line))
        if tag == "a" and values.get("href") is not None:
            self.items.append((values["href"], False, "", line))

def references(text: str):
    clean = without_code(text)
    definitions, items = {}, []
    for match in DEFINITION.finditer(clean):
        key = " ".join(match[1].casefold().split())
        target = match[2].removeprefix("<").removesuffix(">")
        definitions[key] = target
        items.append((target, False, "", clean.count("\n", 0, match.start()) + 1))
    # Definitions aren't link usages.
    clean = DEFINITION.sub(lambda m: re.sub(r"[^\n]", " ", m[0]), clean)
    occupied = []
    for match in INLINE.finditer(clean):
        target = destination(clean, match.end())
        items.append((target, bool(match[1]), match[2], clean.count("\n", 0, match.start()) + 1))
        occupied.append((match.start(), match.end() + len(target) + 1))
    for match in REFERENCE.finditer(clean):
        key = " ".join((match[3] or match[2]).casefold().split())
        items.append((definitions.get(key), bool(match[1]), match[2], clean.count("\n", 0, match.start()) + 1))
        occupied.append(match.span())
    for match in SHORTCUT.finditer(clean):
        if any(start <= match.start() < end for start, end in occupied):
            continue
        key = " ".join(match[2].casefold().split())
        if key in definitions:
            items.append((definitions[key], bool(match[1]), match[2], clean.count("\n", 0, match.start()) + 1))
    parser = HTMLReferences()
    parser.feed(clean)
    items.extend(parser.items)
    return items

def case_mismatch(path: Path, root: Path) -> bool:
    current = root
    for part in path.relative_to(root).parts:
        if not current.is_dir():
            return False
        names = [child.name for child in current.iterdir()]
        if part not in names and any(name.casefold() == part.casefold() for name in names):
            return True
        current /= part
    return False

def audit(readme: Path, repo_root: Path | None = None, max_asset_mb: float = 2.0) -> dict:
    if not math.isfinite(max_asset_mb) or max_asset_mb <= 0:
        raise ValueError("Asset budget must be positive and finite")
    readme = Path(readme).resolve()
    if repo_root is None:
        repo_root = next((p for p in readme.parents if (p / ".git").exists()), readme.parent)
    root = Path(repo_root).resolve()
    report = {
        "readme": str(readme), "repo_root": str(root),
        "errors": [], "warnings": [], "assets": [], "external_links": [],
        "unchecked": UNCHECKED.copy(),
    }
    seen_issues, assets, external = set(), {}, set()

    def issue(category, code, target, line):
        key = (category, code, target, line)
        if key not in seen_issues:
            report[category].append({"code": code, "target": target, "line": line})
            seen_issues.add(key)

    try:
        if not readme.is_relative_to(root):
            issue("errors", "path_outside_repository", str(readme), 1)
            return report
        text = readme.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError):
        issue("errors", "readme_unreadable", str(readme), 1)
        return report
    for target, image, alt, line in references(text):
        if image and not alt.strip():
            issue("warnings", "empty_alt", target or "", line)
        if target is None:
            issue("errors", "undefined_reference", alt, line)
            continue
        if not target:
            if image:
                issue("errors", "empty_image_target", "", line)
            continue
        if target.startswith("#"):
            continue
        if re.match(r"^[A-Za-z]:[\\/]", target) or target.lower().startswith("file:"):
            issue("errors", "nonportable_target", target, line)
            continue
        try:
            url = urlsplit(target)
        except ValueError:
            issue("errors", "invalid_target", target, line)
            continue
        if url.scheme or url.netloc or target.startswith("//"):
            external.add(target)
            continue
        decoded = unquote(url.path)
        if "\\" in decoded:
            issue("warnings", "nonportable_separator", target, line)
            decoded = decoded.replace("\\", "/")
        anchor = root if decoded.startswith("/") else readme.parent
        candidate = Path(os.path.abspath(anchor / decoded.lstrip("/")))
        resolved = candidate.resolve()
        if not resolved.is_relative_to(root):
            issue("errors", "path_outside_repository", target, line)
            continue
        try:
            wrong_case = case_mismatch(candidate, root)
            if wrong_case:
                issue("errors", "case_mismatch", target, line)
                continue
            if not candidate.exists():
                issue("errors", "missing_local_target", target, line)
                continue
            if image and not candidate.is_file():
                issue("errors", "image_is_not_file", target, line)
                continue
            if image and candidate.suffix.lower() in IMAGE_EXTENSIONS:
                size = candidate.stat().st_size
                assets[str(candidate)] = {"path": str(candidate.relative_to(root)), "bytes": size}
                if size > max_asset_mb * 1024 * 1024:
                    issue("warnings", "large_asset", target, line)
        except OSError:
            issue("errors", "target_unreadable", target, line)
    report["assets"] = sorted(assets.values(), key=lambda item: item["path"])
    report["external_links"] = sorted(external)
    return report

def positive(value: str) -> float:
    number = float(value)
    if not math.isfinite(number) or number <= 0:
        raise argparse.ArgumentTypeError("must be a positive, finite number")
    return number

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("readme", type=Path)
    parser.add_argument("--repo-root", type=Path)
    parser.add_argument("--max-asset-mb", type=positive, default=2.0, help="per-image warning budget in MiB")
    parser.add_argument("--json", action="store_true", help="JSON output (the default)")
    parser.add_argument("--strict", action="store_true", help="also fail on warnings")
    args = parser.parse_args()
    report = audit(args.readme, args.repo_root, args.max_asset_mb)
    print(json.dumps(report, ensure_ascii=True, indent=2))
    return int(bool(report["errors"] or (args.strict and report["warnings"])))

if __name__ == "__main__":
    raise SystemExit(main())
