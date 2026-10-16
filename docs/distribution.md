# Distribution and installation

The first channel is a Git-backed marketplace shared by Codex and Claude Code.
Both catalogs are `innosquad`; the plugin ID is `innosquad@innosquad`. Relative
`./` sources load the plugin from the same fetched revision, including resources
and notices. Sources: [OpenAI packaging](https://developers.openai.com/plugins/build/plugins)
and [Claude marketplaces](https://code.claude.com/docs/en/plugin-marketplaces).

The repository is currently private. Review-branch access is not public
publication; a Git marketplace is separate from an official-directory listing.
For Grok CLI, Grok web/app/API, Gemini CLI, Cursor and Copilot, use the additional
[host delivery paths](host-support.md), sharing the original library skill folders.

## Review the candidate

For development or review builds, clone the PR branch and install the local catalog:

```bash
git clone --branch codex/innodi-skill-pilot https://github.com/InnoSquadCorp/innosquad-agent-skills.git
cd innosquad-agent-skills
git rev-parse HEAD
python3 -B scripts/validate_bundle.py
codex plugin marketplace add .
codex plugin add innosquad@innosquad
claude plugin marketplace add "$PWD"
claude plugin install innosquad@innosquad --scope user
```

Record the fetched commit. Codex can fetch an immutable Git source directly with
`codex plugin marketplace add InnoSquadCorp/innosquad-agent-skills --ref COMMIT_SHA`.
For release installation, use the immutable tag procedure below only once that
tag exists. Start a fresh host session after installation/update.

## Install v1.0.0 after publication

Use this procedure only after the reviewed [v1.0.0 Release](https://github.com/InnoSquadCorp/innosquad-agent-skills/releases/tag/v1.0.0)
is published and its immutable tag/commit and checksums are verified:

```bash
git clone --branch v1.0.0 --single-branch https://github.com/InnoSquadCorp/innosquad-agent-skills.git innosquad-agent-skills-1.0.0
cd innosquad-agent-skills-1.0.0
git rev-parse HEAD
python3 -B scripts/validate_bundle.py --require-merged
codex plugin marketplace add .
codex plugin add innosquad@innosquad
claude plugin marketplace add "$PWD"
claude plugin install innosquad@innosquad --scope user
```

Compare the fetched commit to the release's recorded commit. An extracted native
plugin ZIP can also be validated/installed from its `innosquad/` directory. It
contains both marketplace catalogs; `references/innosquad-skills.zip` instead
contains standalone skills and is not the full plugin.

## Move from the local pilot

alpha.11 used `innosquad@innosquad-local`. Install and verify the new identity,
then disable the old one to avoid duplicate discovery. Preserve the old cache
until the new installation works.

For Claude: `claude plugin disable innosquad@innosquad-local --scope user`.
For Codex, disable the old plugin in desktop settings; the corresponding key is
`[plugins."innosquad@innosquad-local"]` with `enabled = false`. Do not replace
the user's full configuration or remove unrelated marketplaces.

## Consumer validation

The [six-consumer CI](consumer-ci.md) resolves, builds and tests every unchanged
library-owned fixture on the explicit Xcode 27.0 / Swift 6.4 / macOS 27 runner.
Each consumer uses a fresh external scratch directory and preserves toolchain,
exact dependency identities and failure artifacts. Missing prerequisites fail;
Python mock tests and bundle checks do not stand in for these Swift results.
Router's upstream fixture retains exact 7.0.0; the central `router-7.0.1` case
separately verifies published 7.0.1 with isolated inputs and tag checks.
Protobuf's reviewed reissued release uses
the existing release mode:

```bash
python3 skills/innonetwork-protobuf/scripts/validate_consumer.py \
  --release-tag 6.1.1 \
  --expected-adapter-revision ba6ab8d6112d51efa69d92ac6739464bfc775aed \
  --expected-tag-object eaea83c7f95f931b6e963c49ae10c7ef5f869438 \
  --scratch-path /tmp/protobuf-skill-release
```

The source fixture stays historical. This qualifies the current release only if
both remote identity checks, graph checks and Swift tests pass. Warm caches must
have their actual checkout identities verified.

## AI host evaluation

Use isolated consumer workspaces and fresh installed-plugin sessions. Supply the
task and manifest/lock scaffold, not answers or grading criteria. Keep raw traces
outside this repository and commit sanitized summaries. Independently compile
generated sources without manual repair. Separate model corrections, harness
failures and implementation failures.

Noninteractive Claude's `acceptEdits` does not grant external reference reads or
build commands. Use `--add-dir` for the installed skill directory and exact cache,
and `--allowedTools` for needed read/build/test commands. Restrict requested
writes to the isolated Sources/Tests. Do not use blanket permission bypass or
alter authentication. Registration, actual selection and generation are separate.

## Publication handoff

Use the [1.0.0 preparation checklist](release-1.0.0.md) and draft
[release notes](release-notes-1.0.0.md). All six canonical correction PRs are
merged, as recorded in the [source status snapshot](release-status-1.0.0.json)
and current `sources.lock.json`. Router's skill source has subsequently advanced
to the immutable published 7.0.1 commit, with its 7.0.0 baseline preserved.
The exact source pins agree. Complete the central PR and initial private
release procedure separately. Recheck upstream status, source-tree
equality and final central CI before packaging. `--require-merged` checks
recorded statuses, not live remote CI. Candidate packaging remains available:

```bash
python3 -B scripts/build_release.py --candidate --output artifacts/1.0.0-candidate
```

After source verification, final commit and clean-worktree validation, omit `--candidate`
to build the merged-source package. Neither command publishes. Repository
visibility, merges, immutable tag, GitHub release and directory submission remain
separate publication actions with their own evidence.

An OpenAI directory submission is a separate review with additional presentation
requirements: [submission guide](https://developers.openai.com/plugins/deploy/submission).
This Git marketplace package does not claim official-directory approval.
