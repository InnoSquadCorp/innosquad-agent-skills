# InnoSquad Agent Skills 1.0.0

Published on 2026-10-16. The repository and release are public; see
[publication, content-review and anonymous-delivery evidence](release-verification-1.0.0.json).

Six library-owned skills packaged for Codex and Claude Code, with portable delivery
for Gemini CLI, Cursor, GitHub Copilot, Grok and text-based assistants.

- InnoDI 7.0.x, InnoNetwork 6.1.x, InnoFlow 6.0.x, InnoRouter 7.0.x and
  InnoNetwork-Protobuf 6.1.x. Exact tested baselines are recorded in each skill.
- InnoNetwork-Stream supports stable 6.1.x with a verified published 6.1.1
  consumer and exact Core 6.1.1. Other patches require their own consumer checks.
- Complete instructions, references, consumer examples, validation scripts and
  original notices. Library choices and existing project configuration are preserved.
- Consumer validators keep JSON output separate from SwiftPM warning diagnostics.
- Router's skill source is released 7.0.1. The original 7.0.0 fixtures remain intact,
  with a separate central-owned exact-7.0.1 tag/resolve/build/test case.
- Deterministic plugin/reference archives, source provenance and SHA-256 checksums.

Model support is evidence-based: Codex has a passing representative DI evaluation;
Claude has dated successful native evaluation and a later authentication-blocked
probe. Gemini CLI 0.24.0 requires Agent Skills to be enabled. Gemini/Cursor fresh
generation remains unverified. Copilot loads the skills, but GPT-4.1 failed the
recorded generation evaluation. Grok has format/offline checks, not a live-model
qualification. See the host support and evaluation documents before adoption.

Patch-line support is not a claim that every patch, model, device or live service
has been tested. Web Markdown is supplied reference context, not a native web
plugin. Generated code must be validated in the actual consumer project.

PR #1 merged at `0c59bbd03541ff1d808e0d7a0efd2d9189e73ece`. PR, merged-main
and tag CI each passed seven consumers and 83 Swift tests; the tag workflow
also passed 50 bundle tests and the merged-source packaging gate.
All thirteen assets matched draft, published and anonymous downloads. The
annotated tag and immutable builder records were preserved through publication.
