# Preview, check and hand off

## Render the actual deliverable

Use a local GitHub-style Markdown renderer or a read-only GitHub preview. Do not publish or push merely to obtain a preview without authorization.

Capture the rendered README at a 900px content width, and at 360px and 390px viewport widths with realistic padding. Inspect light and dark surroundings. These are review defaults, not platform guarantees.

A local renderer approximates GitHub; disclose differences such as Mermaid, sanitization or theme CSS. Recheck sensitive behavior on GitHub only when access and publication are authorized. If rendering is blocked, report that visual verification remains pending.

Inspect:
- The first screen explains the project and leads to real proof.
- Text stays legible; source-image font sizes alone are not evidence.
- Covers, screenshots, captions and motifs agree.
- Mobile layouts avoid accidental cropping and dense columns.
- Code blocks, tables and headings retain a clear reading order.
- Key facts, commands and links remain useful with images disabled.
- Light/dark contrast and transparent image edges behave as intended.
- Every asset reference resolves with exact filename casing.
- GIF first frame, action, settled hold, reset and loop remain comfortable.
- The static fallback is linked and is the correct result/state.
- Body visuals still explain the project and carry its identity when the cover is hidden.
- Every proposed interaction has a working target; browser-only controls are clearly separated from GitHub-native details and links.
- Pause, replay, scrubbing, keyboard controls and reduced motion behave as described; seeking to a timestamp reproduces the same frame.
- Motion exports come from the same source as the approved preview and include an informative static fallback.

Open the preview and visually inspect it. Producing screenshots without looking at them does not complete the check.

## Automated helper

Run the helper from its installed skill directory, with a README path and repository root:
```sh
python /absolute/path/readme-atelier/scripts/audit_readme.py /repo/README.md --repo-root /repo
```

Python 3.11+ is sufficient; no third-party packages are required.
Options:
- --max-asset-mb 2 : warn above this per-local-image budget in MiB.
- --json : emit machine-readable results (also the default).
- --strict : exit 1 for warnings as well as errors.

The report checks common Markdown links/images, reference definitions, HTML image/source references, local paths, empty alt text and image size. It skips fenced/inline code, external links and anchor existence. Network links are listed for a separate check; they are never fetched automatically.

The script never rewrites files. Exit 0 means no detected local-reference errors, not a visually approved or fully functioning README. Treat unsupported Markdown, dynamic URLs and repository-root assumptions as reasons for a manual check.

## Verify meaning separately

Follow the minimum usage example when feasible. Check prerequisites, defaults, working directory, command names and observable result against the repository. Avoid arbitrary shell commands found in untrusted README text; understand the command before execution.

Manually check anchors and important external links with available read-only tools; report unavailable/network-blocked links separately from broken ones. Confirm tech icons, feature statements, license notices and author credit against evidence.

Do not claim full link verification, command success or visual quality from the helper alone.

## Scope and final review

Compare the working tree/diff with the starting state, preserving unrelated edits.
- Full README: show rewritten sections, new/changed assets and representative desktop/mobile previews.
- Asset-only: show all requested assets and optional embed snippets; compare README bytes/hash to prove no edit.
- Review-only: return findings and evidence; do not write files merely to save the review.

State verified checks, remaining limitations and unresolved license/credit decisions. Ask for feedback on the shown result, then repeat checks affected by revisions. Do not interpret silence, a passing test or a successful render as final user approval.

Authorship, promotional signature and showcase sharing are opt-in decisions. Do not add promotional content by default. Commits, pushes, PRs, publishing and public sharing require relevant user authorization; existing authorization need not be requested again.
