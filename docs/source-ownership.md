# Library-owned skills, centrally assembled plugins

The source of truth for each library skill lives in the library's repository.
This repository collects reviewed snapshots and owns their distribution as
Codex and Claude Code plugins. All six planned library skills now have library-owned sources: InnoDI,
InnoNetwork, InnoFlow, InnoRouter, InnoNetwork-Protobuf and InnoNetwork-Stream.

## Responsibilities

| Location | Maintains |
| --- | --- |
| `InnoSquadCorp/InnoDI`, `skills/innodi/` | InnoDI skill, discovery metadata, 7.0.x guidance with 7.0.0 baseline references, support record, consumer fixture, validation helper and license notice |
| `InnoSquadCorp/InnoNetwork`, `skills/innonetwork/` | InnoNetwork skill, discovery metadata, 6.1.x guidance with 6.1.0 baseline references, support record, consumer fixture, validation helper and license notice |
| `InnoSquadCorp/InnoFlow`, `skills/innoflow/` | InnoFlow skill, discovery metadata, 6.0.x guidance with tagged 6.0.0 baseline, support record, consumer fixture, validation helper and license notice |
| `InnoSquadCorp/InnoRouter`, `skills/innorouter/` | InnoRouter skill, discovery metadata, planned 7.0.x guidance with an exact unreleased-main baseline, consumer fixture, validation helper and license notice |
| `InnoSquadCorp/InnoNetwork-Protobuf`, `skills/innonetwork-protobuf/` | Protobuf skill, discovery metadata, stable 6.1.x guidance with exact adapter/Core 6.1.1 baseline, consumer fixture, graph validator and license notice |
| `InnoSquadCorp/InnoNetwork-Stream`, `skills/innonetwork-stream/` | Stream skill, discovery metadata, planned stable 6.1.x guidance with exact unreleased main/Core 6.1.1 baseline, consumer, validator and notices |
| This repository | Plugin manifests, catalogs, installation/update behavior, host selection and generation evaluations, future cross-library integration guidance |
| This repository's `skills/` | Copies of exact source snapshots, refreshed together with the lock record; no independent edits |

Changing a library API and its skill in the same PR makes their relationship
reviewable. A supported-library record names the exact release/revision tested. When the user
explicitly targets a planned release, pin an immutable unreleased commit and mark
that status throughout. Presence in `main`, a runtime version string or release
notes does not prove publication or qualify the eventual tag.

## Two independent versions

The **skill source commit** identifies the instructions and assets to collect.
The **validated library release/revision** identifies the API those assets
were tested against. They need not be the same commit. An instruction fix can
therefore be distributed without publishing a new Swift library release.

[sources.lock.json](../sources.lock.json) records both, along with the source
path and its Git tree identity. This file is a distribution record, not a
second source for API support: `library.version/revision` name the tested baseline;
optional support-range fields declare intended stable versions. For an unreleased
baseline, `version` is null and `planned_version`, `baseline_kind`, and `support_status`
make that boundary explicit. All library fields
must agree with the copied
`references/support.json`.

## Update process

1. Change guidance and the relevant consumer fixture in the library repository.
   Run the consumer validation and any necessary behavioral evaluation.
2. Select an exact source commit, retain the source license, and copy the full
   skill directory. Do not fetch a moving `main` as a release input or use a
   cross-repository symlink that breaks outside the authoring machine.
3. Update the lock record and verify path set, bytes, and file modes against
   the source tree. Remove obsolete files only within that skill's snapshot.
4. Validate both plugin formats and installation behavior. Repeat AI
   selection/generation checks when instructions or discovery metadata change.
   Mark reused evidence separately from new runs.
5. Publish a plugin version only after the selected source is merged and its
   applicable checks are satisfied. Preserve earlier plugin versions and pins.

## InnoDI 7.0.1 source refresh

The initial pilot was transferred to [InnoDI PR #54](https://github.com/InnoSquadCorp/InnoDI/pull/54),
merged on 2026-10-06. Public [InnoDI 7.0.1](https://github.com/InnoSquadCorp/InnoDI/releases/tag/7.0.1)
includes the canonical skill. The alpha.6 snapshot pins release commit
`ce47cf4b207c3b8810b2a7d7d622a2f8ead3ed96` and the 14-file skill tree
`aa58cff138c95a3a5af4949a55a460ca253f0435`. Its source status is `released`;
the PR link remains provenance. All paths, bytes and modes match that release.

Stable `>=7.0.0, <7.1.0` is the supported range. The exact bundled consumer and
`library.version/revision` remain the validated 7.0.0 baseline. Separate tests
against actual 7.0.1 do not rewrite the canonical fixture or historical records.
See [the alpha.6 host and consumer evidence](host-evaluation-innodi-7.0.1.md).

The prior alpha.5 snapshot pinned pre-merge source `ef23b1e`. That input and
its earlier host results remain in Git history and dated reports. Automatic
collection, source-update PRs, and publication CI are not implemented;
this refresh was performed explicitly. Public plugin distribution remains pending.

## InnoNetwork 6.1.x support

[InnoNetwork PR #148](https://github.com/InnoSquadCorp/InnoNetwork/pull/148)
adds the library-owned skill on the published 6.1.0 baseline. Its source commit
and 13-file runtime tree are pinned in the same lock. The central snapshot is
copied explicitly and compared by path, bytes and mode. Its alpha.5 source pin
is unchanged in alpha.6, which includes both skills. Installation and representative
AI results are recorded in [the Network host evaluation](host-evaluation-innonetwork.md).
The Network source remains under PR review; the DI source is now a released snapshot.
No public plugin publication is implied.

The Network support declaration covers stable `>=6.1.0, <6.2.0`, while its exact
consumer and evidence remain pinned to 6.1.0. Future stable patches are handled
against the consumer's actual resolved version; they are not automatically added
to the set of tested releases.

## InnoFlow 6.0.x support

[InnoFlow PR #57](https://github.com/InnoSquadCorp/InnoFlow/pull/57) owns the
14-file Flow skill. Alpha.7 copies source `9dee939ea4e4b0d84609351e046bfc70dfc9d95e`,
tree `51eab5f99de25af4574e6b9d54a01191da90b866`, with exact path/byte/mode equality.
The source remains under PR review; it is not part of the existing library tag.

Supported stable versions are `>=6.0.0, <6.1.0`; prereleases and 6.1+ need separate
source review. The exact validated tag is 6.0.0 at
`188c2732d26350cf01afadade3dac89a2b73b68f`. No corresponding GitHub Release page
was found at the check. A later 6.0.x consumer keeps its patch and receives
patch-specific checks; neither support range nor a tag alone proves its tests passed.

Alpha.7 preserves the DI and Network source pins and runtime files. Fresh Flow
installation and representative AI results are recorded in
[the Flow host evaluation](host-evaluation-innoflow.md). These are local pilot
updates; automatic snapshot collection and public plugin publication remain pending.

## InnoRouter planned 7.0.x support

[InnoRouter PR #66](https://github.com/InnoSquadCorp/InnoRouter/pull/66) owns the
14-file Router skill. The PR merged on 2026-10-07. Alpha.8 pins merge commit
`3ed5ea0d6b07c1b282182c6e5468dd3ed962c402`,
tree `eac03752e4acf3b9329846f2cc6002a05d5a5718`, and copies every path, byte and mode.
Its tree matches evaluated source `f790079eb7a6465bacf69946eac332e9df4028c3`
exactly and is present in origin/main. Merged source does not establish a release.

The user selected current main as the intended 7.0.0 API. The library baseline is
unreleased `851c63f095e49b700c3a0aa8152a3521a39977e7`; the 7.0.0 tag was absent at
check. Planned stable support is `>=7.0.0 <7.1.0`, excluding prereleases. The
fixture uses a remote revision requirement, not moving main or a nonexistent tag.
When 7.0.0 ships, verify its actual commit, inspect differences and rerun the
exact-tag consumer before updating the source record to a released baseline.
A later 7.0.x consumer keeps its patch and receives patch-specific validation.

Alpha.8 preserves the DI, Network and Flow source pins and runtime files. Their
historical behavioral reports remain dated evidence. Fresh Router installation
and generation results are in [the Router host evaluation](host-evaluation-innorouter.md).
The merged source is verified independently of the still-unreleased library baseline.
No library release, public plugin publication or automated collection is implied.

## InnoNetwork-Protobuf 6.1.x support

[Protobuf PR #7](https://github.com/InnoSquadCorp/InnoNetwork-Protobuf/pull/7) owns
the 13-file `innonetwork-protobuf` runtime skill. Alpha.10 pins source
`10721888976bea9d619cb66f2d2a57fd932a41f1`, tree
`2f0958d5095a396b4c77ef191cd1938110dd2ad7`. The skill source is under PR review;
it is not included in the existing 6.1.1 adapter tag.

The independently validated library baseline is the annotated 6.1.1 tag at
`5e5f8316c94358235c3997e70e5e97aadc11df3a`, which also matched origin/main when
work began. Its manifest requires exact Core 6.1.1 at
`44e4ca28c50c03f817231a077c0f3bdfdbc859c8`. The Core GitHub Release is published;
no adapter GitHub Release page was found at check. Tag identity, release page,
source-skill merge and public plugin publication are separate facts.

Declared stable support is `>=6.1.0 <6.2.0`, excluding prereleases. No adapter
6.1.0 tag was found; the range does not invent one or certify future patches.
Retain the consumer's actual patch, inspect that adapter's Core constraint and
relevant API changes, and test before qualifying another pair. Do not upgrade
Core independently of the adapter's exact dependency requirement.

Alpha.10 preserves all four earlier runtime snapshots and source pins. Fresh
Protobuf [host evaluation](host-evaluation-innonetwork-protobuf.md) is separate
from their dated reports and the source-owned exact-tag consumer evidence.
Snapshots are explicitly collected and compared; automated collection and
public plugin distribution remain pending.

## InnoNetwork-Stream planned 6.1.x support

[Stream PR #9](https://github.com/InnoSquadCorp/InnoNetwork-Stream/pull/9) owns
the 13-file runtime skill. The PR merged on 2026-10-09 (KST) during evaluation.
Alpha.11 pins merge commit `81f945f751090aed7c696e4c453816e01df5dd93`, tree
`e0265a81762cd94656c16f53b466faa93c3b1e36`. This exactly matches evaluated source
`bc8b79ea7a96adc4185493115536fcedebbc23b6`; no instructions, code or fixture
changed. Source merge is independent of library release qualification.

The exact validated library baseline is unpublished main
`bd50e877644ded1b739f66bdd8fb604908606e4b`, intended for 6.1.1; no Stream tag or
GitHub Release was found at check. `version: null`, `planned_version: 6.1.1`,
`unreleased_main_commit` and `planned_stable_line` preserve that boundary.
Declared support is stable `>=6.1.0 <6.2.0`, excluding prereleases, not all 6.x.
The fixture requires the immutable remote revision and exact published Core
6.1.1 (`44e4ca28c50c03f817231a077c0f3bdfdbc859c8`). Support for Stream patches
does not permit arbitrary Core upgrades. Verify actual tag/source differences
and rerun a tagged consumer when Stream ships; preserve and check later patches
against their selected manifest and public API.

The [source validation](https://github.com/InnoSquadCorp/InnoNetwork-Stream/blob/bc8b79ea7a96adc4185493115536fcedebbc23b6/skills/validation.md)
and [fresh host evaluation](host-evaluation-innonetwork-stream.md) separate
consumer, installation and behavioral evidence. Alpha.11 preserves the other
five runtime snapshots/pins and their historical reports. Snapshot collection
is explicit; no automatic collection or public plugin publication is implied.
