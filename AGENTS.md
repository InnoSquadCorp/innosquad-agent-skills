# Repository responsibilities

- Library repositories own skill instructions, references, scripts, and consumer fixtures. `skills/` here contains distribution snapshots, not an independent authoring source.
- Before changing a bundled skill, read `sources.lock.json` and `docs/source-ownership.md`. Make the source change in the owning library repository, then refresh and compare the full skill directory with the pinned source commit.
- This repository owns plugin manifests, marketplace catalogs, cross-library guidance, and host installation/selection evaluations. Keep root, Codex, and Claude identity/version metadata aligned.
- Preserve the source's license notice and keep all runtime resources inside the skill directory. Never bundle local build output, credentials, or private evaluation traces.
- A review-branch source pin is not a merged or released source. Do not describe automated collection or public distribution as implemented until it is actually validated.
