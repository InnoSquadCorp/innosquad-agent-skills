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

| Skill | alpha.12 source selection | API evidence |
| --- | --- | --- |
| DI | Published 7.0.1 `ce47cf4` | Exact 7.0.0 fixture; earlier separate 7.0.1 check retained |
| Network | Published 6.1.1 `44e4ca2`, unchanged runtime tree | Exact 6.1.0 fixture |
| Flow | Published 6.0.2 `1176de1`, includes bounded validator | Exact 6.0.0 fixture rerun |
| Router | [PR #69](https://github.com/InnoSquadCorp/InnoRouter/pull/69), exact pin in lock | Published 7.0.0 `33b0da7`, fresh exact-tag consumer |
| Protobuf | Reissued 6.1.1 `ba6ab8d` | Fresh reissued-tag consumer; withdrawn-tag fixture retained as historical |
| Stream | Merged PR #9 `81f945f`, unchanged skill tree | Unreleased `bd50e87`, planned 6.1.1, exact Core 6.1.1 |

The old Network, Flow and Protobuf PRs all merged. Router PR #69 is a new update,
distinct from original merged PR #66. Its source remains under review until the
actual merge is verified. `source_status: released` means the skill is in the
recorded source release; it does not qualify every supported patch.

The original Protobuf 6.1.1 tag pointed to `5e5f831`. Upstream withdrew it and
published `ba6ab8d` with annotated tag object
`eaea83c7f95f931b6e963c49ae10c7ef5f869438`. The source intentionally retains its
old fixture as `historical_revoked_release_tag`. Release-mode validation seeds
only the isolated adapter revision, verifies the official tag before/after
execution and checks all eight remote dependencies. Never call the old fixture
validation of the reissued tag or independently upgrade exact Core 6.1.1.

Stream has no published tag at the 2026-10-09 check. A plugin alpha can explicitly
include that planned baseline; this does not qualify a released Stream 6.1.1.

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
[alpha.12 report](release-candidate-alpha.12.md) for current evidence.
