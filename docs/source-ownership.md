# Library-owned skills, centrally assembled plugins

The source of truth for each library skill lives in the library's repository.
This repository collects reviewed snapshots and owns their distribution as
Codex and Claude Code plugins. The decision applies to all six planned Inno
library skills; only InnoDI is implemented so far.

## Responsibilities

| Location | Maintains |
| --- | --- |
| `InnoSquadCorp/InnoDI`, `skills/innodi/` | InnoDI skill, discovery metadata, exact-version API references, support record, consumer fixture, validation helper and license notice |
| Other library repositories, when implemented | Their own skill and library-specific consumer validation |
| This repository | Plugin manifests, catalogs, installation/update behavior, host selection and generation evaluations, future cross-library integration guidance |
| This repository's `skills/` | Copies of exact source snapshots, refreshed together with the lock record; no independent edits |

Changing a library API and its skill in the same PR makes their relationship
reviewable. A supported-library record still names the exact public release
and revision that was tested; presence in a library's `main` does not mean the
skill's examples support unreleased APIs.

## Two independent versions

The **skill source commit** identifies the instructions and assets to collect.
The **supported library release/revision** identifies the API those assets
were tested against. They need not be the same commit. An instruction fix can
therefore be distributed without publishing a new Swift library release.

[sources.lock.json](../sources.lock.json) records both, along with the source
path and its Git tree identity. This file is a distribution record, not a
second source for API support: its library fields must agree with the copied
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

## Current migration state

The initial pilot was authored here. Its 14 runtime files have now been
transferred to [InnoDI PR #54](https://github.com/InnoSquadCorp/InnoDI/pull/54)
based on public 7.0.0. The redistribution notice
was updated for InnoDI's MIT license; instructions, discovery metadata,
references, script, and Swift fixture were preserved. The current bundled
copy matches that exact source commit, recorded as `pull_request` in the lock.
That status is not evidence that the source PR has merged or entered a release.

The existing host evaluation reports remain here as historical evidence.
InnoDI owns its fresh consumer evidence. Automatic collection, source-update
PRs, and publication CI are **not implemented by this migration**; the initial
snapshot refresh and equality checks were run explicitly. After the source PR
merges, refresh the pin to the merged commit and change its status only after
checking the actual remote state. Public distribution remains pending.
