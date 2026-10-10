# InnoSquad Agent Skills 1.0.0

Draft release notes — not published.

Six library-owned skills packaged for Codex and Claude Code, with portable delivery
for Gemini CLI, Cursor, GitHub Copilot, Grok and text-based assistants.

- InnoDI 7.0.x, InnoNetwork 6.1.x, InnoFlow 6.0.x, InnoRouter 7.0.x and
  InnoNetwork-Protobuf 6.1.x. Exact tested baselines are recorded in each skill.
- InnoNetwork-Stream supports stable 6.1.x with a verified published 6.1.1
  consumer and exact Core 6.1.1. Other patches require their own consumer checks.
- Complete instructions, references, consumer examples, validation scripts and
  original notices. Library choices and existing project configuration are preserved.
- Consumer validators keep JSON output separate from SwiftPM warning diagnostics.
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

Publication must wait for the preparation checklist's source merge, final commit,
CI and intended-audience conditions. Remove this draft-only publication note only
after those conditions and the actual release action are complete.
