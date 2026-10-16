# InnoNetwork host evaluation — 2026-10-07

This adds the published **InnoNetwork 6.1.0** skill to the existing InnoDI pilot.
The source release is `79ff9f535a0a15ad8b52ce49cb5a4b1ea1dfec16`.
[sources.lock.json](../sources.lock.json) pins the skill source independently;
[InnoNetwork PR #148](https://github.com/InnoSquadCorp/InnoNetwork/pull/148)
owns its instructions, fixture and fresh 13-test consumer evidence.

## Installation and packaging

Both hosts were updated through their native plugin commands from alpha.2 to
alpha.3, then alpha.4 after the JSON-header correction below. Earlier caches were
preserved. The initial generation pilot was `innosquad@innosquad-local` **0.1.0-alpha.4**.

| Check | Fresh result |
| --- | --- |
| Portable manifest JSON schema and three host identity fields | PASS |
| Claude marketplace validation | PASS; optional marketplace-description warning |
| Claude plugin manifest validation | PASS |
| Codex CLI 0.160.1 native installation | PASS, alpha.4 installed/enabled |
| Claude Code 2.1.285 native update | PASS, alpha.4 user scope |
| Installed runtime snapshots | Both hosts match central path/bytes/modes for InnoDI and InnoNetwork |
| Library source snapshot | 13 InnoNetwork files match pinned source Git tree; InnoDI's 14-file source pin is unchanged |
| Claude skill registration | Fresh alpha.3 startup listed both `innosquad:innodi` and `innosquad:innonetwork` |
| Claude AI execution | BLOCKED: OAuth 401, invalid access token; no generated consumer or behavior pass |

Alpha.4 has only the JSON-header guidance/fixture correction relative to alpha.3.
Its installed cache equality was verified in both hosts. Claude behavior was not
retried after the authentication failure, and is not inferred from registration.
The previously recorded [InnoDI AI results](host-evaluation.md) are reused
historical evidence, not a fresh DI run on alpha.4.

## Codex selection and generated consumers

Fresh ephemeral CLI sessions used the configured `gpt-6-astra` / `xhigh` settings,
with prior conversation and memory disabled. Other plugins, MCP servers and
39 local/system skill paths were disabled through per-command overrides; global
settings were not changed. Both Inno skills remained installed. This isolates
selection within the plugin; it does not qualify a full everyday plugin profile.

The model was asked to create source/tests while preserving the supplied manifest
and lock, and to leave builds to the evaluator. Generated output was then compiled
**without manual code edits** using strict concurrency and warnings as errors.
The two networking packages retained exact remote 6.1.0 pins; actual checkout
SHAs and clean state were checked independently. No live service was contacted.
Prompts and acceptance criteria are in [evals/innonetwork.json](../evals/innonetwork.json).

| Case | Installed version | Selection | Independent result |
| --- | --- | --- | --- |
| Korean JSON GET/POST, initial attempt | alpha.3 | Implicit skill read confirmed | Build passed; 1 of 2 tests failed on an overstrict Content-Type assertion |
| Same Korean request in a fresh session | alpha.4 | Implicit skill read confirmed | PASS, 2 tests with multiple IDs and escaped/Unicode names |
| English buffered encoded request | alpha.3 | Explicit skill read confirmed | PASS, 4 tests: byte reuse, fresh invocation, codec failure, retry budget |
| Unrelated string formatting | alpha.3 | No Network skill read or dependency addition | PASS, 2 tests including parameterized cases |

The initial generated JSON test assumed `Content-Type == "application/json"`.
The public encoder correctly produces `application/json; charset=UTF-8`.
This was a generated test defect, not a library failure. The source reference
and fixture now state/assert that contract, and the 13-test fixture
passed after adding the assertion. Alpha.4 was installed before rerunning the
**same prompt from a clean workspace**, without supplying the earlier answer or
failure to that session. The first failure remains part of the evidence.

Sanitized [result metadata](host-evaluation-innonetwork.json) records the observed
versions, statuses and generated source hashes. Raw prompts, transcripts, build
logs and generated files remain in local ReviewArtifacts rather than the plugin.
These are representative single attempts, not a statistical quality score.

## Boundaries

No full bilingual matrix, 6.0-to-6.1 migration execution, combined DI/Network
consumer, optional-product/companion qualification, real service, device or
background lifecycle acceptance was run. Both bundled source inputs are PR
snapshots: Network is still under review, while DI PR #54 merged with a different
skill tree. The previously validated DI snapshot is retained for this addition;
its merged-source refresh remains a separate update. Automatic collection/publication is still unimplemented. Local
installation, local test success, remote CI, source merge and public plugin
publication are separate states; this work does not publish a public plugin.

## Stable 6.1.x support policy — alpha.5

The user requested stable **6.1.x** support ahead of the planned 6.1.1 release.
Alpha.5 separates that range (`>=6.1.0, <6.2.0`, excluding prereleases) from the
validated 6.1.0 baseline. The fixture, exact dependency pins, helper and runtime
API examples are unchanged. The exact-release helper passed 13 tests again;
docs contract sync and skill structure checks passed.

Both hosts were updated through their native plugin commands, and runtime
path/bytes/modes match the central snapshots. Manifest schema/identity and Claude
plugin validation passed. A fresh Codex session implicitly selected the installed
alpha.5 skill for the added `patch-support-policy-ko` case. It correctly stated
that 6.1.1 is supported once stable and published, distinguished the tested 6.1.0
baseline, required patch-specific source/release and consumer checks, and avoided
a fixture-driven downgrade. Manifest/lock files stayed unchanged; there were no
external queries, builds or file edits during this policy-only evaluation.

This is fresh policy reasoning evidence. The previous alpha.3/alpha.4 code
creation results above are reused, not rerun or relabeled as alpha.5 generation
results. Claude behavior was not retried after its earlier authentication error.
No 6.1.1 publication, build or runtime validation is claimed. The new source pin
and support metadata are recorded in `sources.lock.json`; the JSON report retains
the initial evidence and adds a separate `patch_support_update` record.
