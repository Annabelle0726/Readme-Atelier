# Whole-page story, interactions and rendering

## Plan the reading sequence

Before producing a full visual README, map the reader's questions to sections. For each section record its purpose, evidence, medium, interaction and mobile treatment. A useful sequence is identity, proof, first use, mechanism, usage modes and deeper reference; reorder it for the project. Keep essential installation visible and compress details that do not help a first-time reader.

For requests emphasizing visual richness, include meaningful body visuals. Common choices are an actual before/after comparison, a process diagram showing intermediate artifacts, and a deliverables overview. These are options, not a fixed template or mandatory image count. Preserve concise Markdown equivalents and copyable commands.

Show only verified results as evidence. A redesigned sample or proposed future state is a concept until actually implemented. Clearly distinguish an explanatory animation, a sequence of genuine artifacts, and an unaltered operation recording. A parser report proves parser behavior; it does not prove visual design quality.

## Choose meaningful motion

Write the sequence as state changes: input becomes a brief, a brief opens into alternatives, a chosen alternative develops into a readable page, and the page is checked at actual widths. Let the objects persist across stages where useful. Tie emphasis, movement and timing to understanding rather than adding perpetual decoration.

A browser preview may have richer controls than GitHub. Implement pause/play, replay, a labeled timeline and keyboard-accessible stage selection for a seekable explainer. Respect reduced motion and pause when the document is hidden. Keep essential information available without animation.

## Platform contract

| Element | GitHub README | Browser preview |
| --- | --- | --- |
| Static diagrams and screenshots | Repository-relative PNG/SVG with alt text | Same assets or their editable source |
| Animation | GIF with linked static fallback | Time-controlled animation with playback controls |
| Usage choices and advanced details | Native details/summary and ordinary links | Native disclosures, optionally enhanced |
| Navigation | Heading anchors and relative links | Working anchors and actual file targets |
| Custom tabs, sliders and transitions | Export states or link to a separately authorized page | Working JavaScript with clear labels |

Do not draw a button in an image and imply it works. Do not present a local styled preview as exact GitHub rendering. Confirm current renderer support when a capability matters. An independent website is additional scope, not an automatic consequence of an interactive README request.

## A usable rendering mechanism

Choose a source format the available environment can render reliably. Editable SVG, HTML/CSS and canvas can all be appropriate. Keep project-specific art separate from reusable render infrastructure; never impose one visual template on unrelated repositories.

For a deterministic browser animation expose a small contract:

```js
window.readmeAtelier = {
  ready: true,          // only after fonts and necessary images are ready
  duration: 12,         // seconds; finite and positive
  renderAt(seconds) {} // sets the complete scene, independent of prior playback
};
```

The page owns the visual design. The renderer only opens the page, waits for readiness, sets a viewport, seeks exact timestamps and captures the designated scene. Avoid frame capture based on wall-clock sleeps or CSS animations that continue during screenshots. `renderAt()` must set all animated properties, including when seeking backward.

The bundled `scripts/render_scene.mjs` implements this contract using Playwright. It captures a still or a frame sequence without exposing a server publicly. It requires Node.js and an externally installed Playwright package/browser; it is an optional rendering dependency, not installed by the skill. Run `node /installed/skill/scripts/render_scene.mjs --help` for setup and commands. The optional `scripts/assemble_gif.py` uses Pillow to assemble a captured sequence into a GIF. It preserves frame timing and prints export metadata. These helpers render authored scenes; they are not image-generation tools.

For an existing motion setup, reuse its deterministic renderer instead of installing a second stack. Capture a useful settled state as the static fallback. Keep frame exports and exploratory previews in a local draft directory; publish only selected final assets within the user's authorized scope.

## Verify the mechanism and result

- Actually open the preview, operate each control, and inspect mobile layout.
- Seek backward and forward; the same timestamp must reproduce the same scene.
- Export representative frames and inspect them, including the end-to-start transition.
- Measure GIF dimensions, frame count, duration and file size; state which figures are actual measurements.
- Verify the GitHub version with static assets, native disclosures and links independently of the richer preview.
- Include reproduction commands and dependency requirements so another session can update assets without rebuilding the process from memory.
