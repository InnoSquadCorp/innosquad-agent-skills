# Library-owned skills, centrally assembled plugins

The source of truth for each library skill lives in the library's repository.
This repository collects reviewed snapshots and owns their distribution as
Codex and Claude Code plugins. The decision applies to all six planned Inno
library skills; InnoDI, InnoNetwork, and InnoFlow are implemented so far.

## Responsibilities

| Location | Maintains |
| --- | --- |
| `InnoSquadCorp/InnoDI`, `skills/innodi/` | InnoDI skill, discovery metadata, 7.0.x guidance with 7.0.0 baseline references, support record, consumer fixture, validation helper and license notice |
| `InnoSquadCorp/InnoNetwork`, `skills/innonetwork/` | InnoNetwork skill, discovery metadata, 6.1.x guidance with 6.1.0 baseline references, support record, consumer fixture, validation helper and license notice |
| `InnoSquadCorp/InnoFlow`, `skills/innoflow/` | InnoFlow skill, discovery metadata, 6.0.x guidance with tagged 6.0.0 baseline, support record, consumer fixture, validation helper and license notice |
| Other library repositories, when implemented | Their own skill and library-specific consumer validation |
| This repository | Plugin manifests, catalogs, installation/update behavior, host selection and generation evaluations, future cross-library integration guidance |
| This repository's `skills/` | Copies of exact source snapshots, refreshed together with the lock record; no independent edits |

Changing a library API and its skill in the same PR makes their relationship
reviewable. A supported-library record still names the exact public release
and revision that was tested; presence in a library's `main` does not mean the
skill's examples support unreleased APIs.

## Two independent versions

The **skill source commit** identifies the instructions and assets to collect.
The **validated library release/revision** identifies the API those assets
were tested against. They need not be the same commit. An instruction fix can
therefore be distributed without publishing a new Swift library release.

[sources.lock.json](../sources.lock.json) records both, along with the source
path and its Git tree identity. This file is a distribution record, not a
second source for API support: `library.version/revision` name the tested baseline;
optional support-range fields declare intended stable versions. All library fields
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
