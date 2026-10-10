# Library-owned skills, centrally assembled plugins

Each library owns `skills/<library>/`. This repository owns manifests, catalogs,
distribution snapshots and installed-host evaluations. Change API instructions
and examples in the library first; never independently patch the bundled copy.
All six skills have canonical library sources.

## Source and API identities

`sources.lock.json` records the exact skill `revision` and `git_tree` separately
from the `library` baseline/support declaration. A skill-source fix does not
require changing the tested library version. All library fields agree with the
copied support record; the validator understands DI's original range/channel schema.

| Skill | 1.0.0 preparation source selection (2026-10-10 refresh) | API evidence |
| --- | --- | --- |
| DI | Graph-output fix, [PR #59](https://github.com/InnoSquadCorp/InnoDI/pull/59) pending | Exact 7.0.0 fixture |
| Network | Graph-output fix merged, [PR #153](https://github.com/InnoSquadCorp/InnoNetwork/pull/153), `d5213fb` | Exact 6.1.0 fixture |
| Flow | Published API baseline/tag checkout and structured failure diagnostics at `f696e36`, [PR #63](https://github.com/InnoSquadCorp/InnoFlow/pull/63) pending | Published 6.0.2 `1176de1`; support remains 6.0.x |
| Router | Native visionOS canonical-recovery probe and graph-output fix at `b82dc6a`, [PR #70](https://github.com/InnoSquadCorp/InnoRouter/pull/70) pending | Published 7.0.0 `33b0da7` |
| Protobuf | Merged [PR #9](https://github.com/InnoSquadCorp/InnoNetwork-Protobuf/pull/9), `06e091d` | Reissued 6.1.1 consumer; historical fixture retained |
| Stream | Graph-output fix and released baseline merged at `7fb61ac`, [PR #14](https://github.com/InnoSquadCorp/InnoNetwork-Stream/pull/14) | Published 6.1.1 `2af03b2`, exact Core 6.1.1 |

The alpha.14 fix separated JSON output and warnings in all six consumer helpers.
This refresh additionally updates Stream instructions, metadata, exact fixture
pins and release-tag guards from its canonical source. Support ranges are unchanged.
Source tests and maintainer documentation remain outside the distributed skill.
See the [latest Flow/Router follow-up](flow-router-followup-2026-10-10.md) and
[earlier refresh report](release-refresh-2026-10-10.md). Three pins remain
`pull_request`; `--require-merged` must reject them. The Protobuf helper fix is merged but not in
the recorded 6.1.1 release, so its source status is `merged`, not `released`.

The original Protobuf 6.1.1 tag pointed to `5e5f831`. Upstream withdrew it and
published `ba6ab8d` with annotated tag object
`eaea83c7f95f931b6e963c49ae10c7ef5f869438`. The source intentionally retains its
old fixture as `historical_revoked_release_tag`. Release-mode validation seeds
only the isolated adapter revision, verifies the official tag before/after
execution and checks all eight remote dependencies. Never call the old fixture
validation of the reissued tag or independently upgrade exact Core 6.1.1.

Stream 6.1.1 was published at `2af03b2`. The refreshed consumer passed 13 tests
and verified the annotated tag before/after execution on 2026-10-10 KST. This
does not replace source PR CI, device or host behavior evidence. The user accepts
keeping Protobuf 6.1.1 because no earlier installations were made; no tag is
moved or patch release created by this refresh. See the [preparation checklist](release-1.0.0.md).

## Refresh and publish

1. Fix guidance/assets in the owning library and validate the consumer. Open a
   source PR; keep resources self-contained and preserve source notices.
2. Select an immutable source commit and copy its complete skill directory,
   including modes. Update the lock and review removals only within that snapshot.
3. Run bundle validation and rejection controls. Verify the recorded tree against
   the owning Git repository; the local validator detects byte/path/mode drift.
4. Validate both native formats and installation. Rerun selection/generation for
   changed guidance/discovery metadata; label reused evidence separately.
5. Verify actual source merge and applicable remote checks before publication.
   Update pins/status after merge and compare trees. Run
   `python3 -B scripts/validate_bundle.py --require-merged`.
6. Publish only the reviewed plugin commit/version. Library tags, repo visibility,
   GitHub releases and official-directory submissions are separate actions.

Collection is explicit. CI validates package consistency but does not collect
snapshots, call AI hosts or publish releases automatically. Earlier snapshots
and reports remain in Git history and dated `host-evaluation-*` files. Historical
failures are not overwritten by newer passes. Read the
[refresh report](release-refresh-2026-10-10.md) for the latest source/consumer checks;
[alpha.12](release-candidate-alpha.12.md) retains the dated host evaluation.
