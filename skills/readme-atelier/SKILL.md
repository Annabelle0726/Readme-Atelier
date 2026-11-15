---
name: readme-atelier
description: Use when a developer requests a GitHub README redesign, readability review, project-specific cover or visual assets, or a real usage demo for a repository README. Also applies to README Atelier requests in Chinese. Excludes unrelated website design and routine code changes.
---

# README Atelier

Make the project recognizable, understandable and usable. Let repository evidence determine both the story and its visual identity.

## Scope and boundaries

| Request | Deliverable | Permitted README changes |
| --- | --- | --- |
| Full README | Evidence-based content, selected visuals, usage path and previews | Within the requested redesign or refresh |
| Assets only | Requested cover, icons, screenshots, diagrams or demo | None, including embeds, unless separately requested |
| Review only | Findings, evidence and actionable recommendations | None; create no repository files unless requested |

Infer scope from explicit wording; ask one short question only when ambiguous. Read-only inspection is allowed first. Preserve unrelated work and the original language unless asked otherwise.

Use existing decisions and authorization. Never add attribution, promotional backlinks, commits, pushes, pull requests, publication or public sharing without the user's relevant authorization. The skill's own MIT license is not a license choice for any project using it.

## 1. Discover the project

Read [discovery-and-content](references/discovery-and-content.md) before substantial content work. Inspect the current README, repository structure, source/configuration, package metadata, real UI/output, screenshots, examples and license files. Inspect only the context needed for an asset-only task.

Produce a short working brief: audience; problem; verified value; strongest proof; first successful action; verified stack; license status; unknowns. Attach file/command evidence to material claims. Existing README claims also need checking. Do not invent features, usage counts, performance, testimonials or compatibility.

If the app cannot run, use available verified artifacts, identify their limitations and state what was not tested. Never present generated UI or conceptual imagery as a real screenshot.

For review-only requests, report prioritized findings and stop; do not force design selection or production.

## 2. Explore and select

Read [visual-directions](references/visual-directions.md). When no direction has already been chosen, show **2–3 visibly different sketches or previews** before full production. Each must use the same verified project story while differing in composition, information emphasis or visual language, not just colors.

Include a rendered preview, a short rationale, proposed media and tradeoffs for each. State any placeholder or conceptual material. Recommend one, then **wait for the user's choice**. Do not choose from silence or rewrite the full README during this pause. If the user explicitly delegates the choice, choose and explain it; an already approved direction needs no new approval.

If rendering is unavailable, explain the limitation and ask to use text-only concepts; do not call a written style list a visual preview.

## 3. Produce the selected visual system

Read [assets-and-demos](references/assets-and-demos.md) for any visual production.

Design one recognizable first screen or cover from the chosen direction. Choose image generation, editable SVG, real screenshots or composition according to the project's identity and evidence. Use the available image-generation tool for requested generated art; do not require a particular connector or hard-code a tool name. If it is unavailable, use an appropriate deterministic or screenshot-based alternative and disclose the change.

Keep exact copy in editable layout sources and essential explanations in Markdown. Generated artwork may communicate identity; real outputs prove capabilities. Keep supporting modules consistent with this project's selected direction.

Place a small, accurate stack icon row with text labels below the cover in full README work. Derive every icon from verified runtime, language, framework or platform usage; do not pile up transitive dependencies, aspirational tools or decorative status badges.

If meaningful operation or result changes require motion, capture the real process, produce a compact GIF and provide a clearly linked static PNG/SVG fallback. Do not animate decoration merely to satisfy a checklist.

Default repository assets to assets/readme/ unless existing conventions or the user specify another path. Keep useful editable sources. In asset-only mode, provide an embed snippet separately and verify that README bytes did not change.

## 4. Write for first use

For full README work, use the content guidance in [discovery-and-content](references/discovery-and-content.md). Lead with identity, a plain-language value statement and real proof; guide the reader to a minimum working example before advanced detail.

Use short paragraphs, meaningful headings, restrained tables, clear spacing, bounded image widths and readable code blocks. Keep commands, key facts, limitations and links usable when images fail. Do not rasterize the README or put all important information inside pictures.

Include system requirements, install/run commands, configuration, examples, known limitations, authorship, contribution and licensing only as applicable and supported. Verify commands using the repository's actual package manager, versions and entry points; report commands not executed.

Read existing LICENSE/COPYING, package metadata and README notices before describing licensing. Preserve existing notices. If licensing is absent, contradictory or requires a choice, ask the user; continue other authorized work with license status pending. Do not create a license, claim open-source status or choose terms without authorization. Verify author credit from existing evidence or ask when a decision is necessary.

## 5. Preview, verify and iterate

Read [preview-and-review](references/preview-and-review.md). Preview the actual Markdown with GitHub-like rendering at 900px content width and 360–390px mobile widths, plus light/dark surroundings. Inspect rendered covers, screenshots, links, crop, readable labels, wrapping and GIF loop boundaries. These are workflow defaults, not GitHub limits.

Run the read-only helper using its absolute skill path:
```sh
python /path/to/readme-atelier/scripts/audit_readme.py /path/to/repository/README.md --repo-root /path/to/repository
```
The helper checks common local references and asset budgets; it is not a renderer, security scanner or proof of successful usage.

Show previews, changed files and a diff appropriate to scope. Distinguish verified checks from blocked or untested ones. Incorporate feedback, repeat affected checks and hand off the approved work. A successful automated check does not imply user satisfaction or authorize external actions.

## Common mistakes

- Reusing a house template: derive the motif, layout and density from this repository.
- Treating a generated interface as proof: show a real output or label the concept.
- Offering color variations as directions: change composition and reading emphasis.
- Shrinking text to fit a cover: reduce density or move detail to Markdown.
- Improving copy during an asset-only task: deliver the requested asset and separate embed snippet.
- Calling an audit a visual review: open and inspect the actual rendered result.

## Example requests

- "Use $readme-atelier to redesign this README; show three visual directions first."
- "用 $readme-atelier 只做首屏封面，不修改 README。"
- "Use $readme-atelier to review readability only; do not edit files."
