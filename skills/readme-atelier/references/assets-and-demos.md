# Covers, accurate icons and real demonstrations

## Choose the medium

| Medium | Use it for | Keep in mind |
| --- | --- | --- |
| Real screenshot/output | Proof of implemented behavior | Use a real build/example; crop without hiding relevant context |
| Editable SVG | Exact titles, diagrams, geometry and small icons | Avoid scripting, foreignObject, web fonts and external raster references |
| Generated raster artwork | Distinctive identity, material or conceptual illustration | Use available image generation; do not make it evidence of product behavior |
| Composed PNG/WebP | Screenshot or generated subject with exact designed type | Keep layout and source layers for editing |
| GIF plus static image | A meaningful real sequence or result change | Measure loading cost and inspect the loop |

Keep project name, value and key facts in Markdown even when repeated in a cover. Keep exact essential lettering out of generated raster art; add it with editable SVG/layout or Markdown. If a raster composition has lettering, retain its editable source.

Inspect existing images before editing. Preserve real UI state and label samples/demonstration data. Use generated art for identity, never fabricated user counts, results, terminals or product screenshots.

## GitHub-safe assets

Use repository-relative image paths and useful alt text. A 1200px-wide source is a useful starting point, not a required output size. Judge readability after scaling at 900px and 360–390px, not at source resolution.

Keep important content away from crop boundaries. Avoid relying on installed custom fonts; use available system fonts, or preserve necessary display lettering as paths with a text equivalent. Test fallback fonts for non-Latin scripts. Flatten unsupported effects when necessary and retain editable sources.

Publish a composed PNG/WebP when the SVG layout depends on local raster layers. Do not rely on SVG animation, CSS/JavaScript interactions or remote fonts for essential content. Provide a self-contained image and a meaningful textual alternative.

Use simple Markdown or supported HTML image sizing. Supply a stable background or separate theme variants when light/dark surroundings cause poor contrast. Do not change the project style solely to match the Skill's own branding.

Keep final assets in the repository's existing docs/media directory, or assets/readme/. Use descriptive lowercase names. Keep only useful source files and selected deliverables; do not delete user assets or publish raw recordings by accident.

## Stack icons

Verify each technology's role in package files and actual code. A lockfile entry alone is not grounds for an icon. Favor the main language, runtime, framework and essential platform.

Use accurate official or established maintained icons; verify usage terms and attribution requirements. Keep names readable as text or alt labels. Icon licensing is separate from project licensing. Prefer local stable assets when practical; if using an external icon service, check its URL and note the dependency. Do not claim endorsement.

Place the row immediately below the cover for full README work. Keep it short enough to remain readable on a narrow screen; use labeled groups or plain text when wrapping is poor.

## Record a real demonstration

1. Choose a single meaningful input, action and visible result from the running project.
2. Use a reproducible example and existing authorized access. If the project cannot run, request a real recording or use a verified static artifact; do not manufacture an interaction.
3. Capture the actual UI/terminal or sequence of genuine output frames. A clearly labeled explanatory animation may supplement, but cannot replace, real proof.
4. Trim dead time without falsifying behavior. Keep relevant cursor/action context and enough time to read the result.
5. Crop to the communication area and export a GIF with a meaningful first frame.
6. Capture a sharp representative static PNG, or use SVG for a genuine vector result. Link it beside the GIF as "Static demo".
7. Inspect playback and file metadata before embedding.

Start around 6–12 seconds and 10–15 FPS for a simple interaction, then tune to the content. Prefer an informative stop and a comfortable transition back to the start. A real app reset can be shown honestly; an explanatory reset may use a short fade/hold. Do not alter results to force a seamless loop.

Aim for <=2 MiB per GIF where practical; review and explain assets above 5 MiB. These are internal performance budgets, not GitHub upload limits. Reduce area, duration, frame rate or palette after comparing readability. Do not discard important steps merely to meet a numeric target.

Use ffmpeg, Pillow or equivalent tools already available. For ffmpeg, use a generated palette and compare dithering choices; do not install a full animation toolchain for a static-only request. Report the actual dimensions, duration, frame count and file size. Inspect the start, actions, result hold, end and end-to-start transition.

A linked static image remains available even if playback fails; do not promise automatic reduced-motion behavior without testing the renderer.

## Source references

Check current capabilities when a renderer-dependent detail matters:
- [GitHub image and formatting syntax](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)
- [GitHub non-code files](https://docs.github.com/en/repositories/working-with-files/using-files/working-with-non-code-files)
