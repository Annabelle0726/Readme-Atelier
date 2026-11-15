# Repository evidence and readable content

## Inspect with a purpose

Read applicable repository instructions and the working tree first. Use existing project conventions and preserve user edits.

| Question | Useful evidence |
| --- | --- |
| Who is it for, and what problem does it solve? | Existing docs, example tasks, public API, actual UI |
| What is the strongest proof? | Running output, screenshot, example artifact, tested transformation |
| How does first use work? | Entrypoints, package scripts, lockfile, tests, configuration schema |
| What belongs in the stack row? | Source language, direct framework use, runtime and deployment requirements |
| What may be claimed about compatibility? | Declared versions plus actual tests/builds; distinguish the two |
| Who owns it, and under what terms? | LICENSE/COPYING, existing credits, package metadata, user decisions |

Use targeted file reads, not an indiscriminate repository dump. A README is a source of claims, not automatic proof of them. If this is a remote repository, inspect the requested/current branch and files rather than relying on a cached description.

Keep a compact evidence ledger during work: claim; source file or command; observed result; uncertainty. Do not add this internal ledger to the public README unless useful to its readers.

## Select the story

Write a brief that a newcomer can understand:
- Audience and task.
- One-sentence value grounded in implemented behavior.
- Strongest real artifact and why it proves the value.
- One successful first-use action.
- Verified stack and requirements.
- Known limitations and licensing status.

For a CLI, real command/output may be stronger than a simulated UI. For a library, use a minimal import and result. For a visual product, show its real interface. For research, show actual results with method and limitations; do not convert unrun experiments into benchmarks.

## Reading order

Choose sections according to the project, using this as a starting sequence:
1. Name, plain-language value and selected cover.
2. Small, accurate stack row with text labels.
3. Real result or demonstration, with enough prose to understand it.
4. Short description of the problem, core capabilities and relevant limits.
5. Requirements and shortest install-to-success example.
6. Workflow or mechanism only to the depth needed by this audience.
7. Additional configuration, examples and troubleshooting.
8. Existing authorship, contribution route and license status.

A compact project may combine sections. A complex project may link to deeper docs. Do not force a table of contents or a section that has no meaningful content.

## Copy and examples

Keep paragraphs focused; use one idea per paragraph. Prefer specific verbs and observable outcomes to marketing claims. Avoid repeated introductions, unexplained internal names and decorative microcopy.

Keep searchable/copyable information in Markdown: installation, environment variables, commands, defaults, API examples, key diagram relationships and meaningful links. Use fenced code blocks with language labels and real filenames. Long lines in code may require scrolling; shorten the example without changing semantics.

Build one end-to-end example using real sample data. Include prerequisites, working directory, configuration keys with safe example values, command and expected result. Do not create credentials, imply a paid account is free, or run destructive setup. Label expected output as illustrative when not executed. Put optional paths after the first success.

Use a diagram for a relationship or branching workflow that prose does not convey well. Prefer native Mermaid for a small exact diagram when supported; otherwise render an editable SVG plus a text explanation. Keep diagram labels readable at mobile width or split the view.

## License, author and contribution

Check existing license files, SPDX metadata, README statements and notices for agreement. Never replace an existing license during a visual refresh. Different components/assets can have different licenses.

When absent or conflicting, ask one concrete question about the missing decision. Continue other work; leave licensing pending in the draft and report the unresolved choice. Do not call an unlicensed repository MIT, freely reusable or open source.

Respect the author's existing name and credit. Adding the user's identity, an AI label, Skill backlink or a promotional signature is a separate choice. Reuse existing CONTRIBUTING instructions; do not invent maintainer response times or community policies.

This skill's repository is MIT-licensed. That fact supplies no authorization to license a target project or third-party logos, fonts and screenshots under MIT.
