# Distribution and installation

The first channel is a Git-backed marketplace shared by Codex and Claude Code.
Both catalogs are `innosquad`; the plugin ID is `innosquad@innosquad`. Relative
`./` sources load the plugin from the same fetched revision, including resources
and notices. Sources: [OpenAI packaging](https://developers.openai.com/plugins/build/plugins)
and [Claude marketplaces](https://code.claude.com/docs/en/plugin-marketplaces).

The repository is currently private. Review-branch access is not public
publication; a Git marketplace is separate from an official-directory listing.

## Review the candidate

Until the central PR merges, clone its branch and install the local catalog:

```bash
git clone --branch codex/innodi-skill-pilot https://github.com/InnoSquadCorp/innosquad-agent-skills.git
cd innosquad-agent-skills
git rev-parse HEAD
python3 -B scripts/validate_bundle.py
codex plugin marketplace add .
codex plugin add innosquad@innosquad
claude plugin marketplace add .
claude plugin install innosquad@innosquad --scope user
```

Record the fetched commit. Codex can fetch an immutable Git source directly with
`codex plugin marketplace add InnoSquadCorp/innosquad-agent-skills --ref COMMIT_SHA`.
For release installation, replace the branch with a published tag that actually
exists. Once merged, the README's `main` commands become the normal install path.
Start a fresh host session after installation/update.

## Move from the local pilot

alpha.11 used `innosquad@innosquad-local`. Install and verify the new identity,
then disable the old one to avoid duplicate discovery. Preserve the old cache
until the new installation works.

For Claude: `claude plugin disable innosquad@innosquad-local --scope user`.
For Codex, disable the old plugin in desktop settings; the corresponding key is
`[plugins."innosquad@innosquad-local"]` with `enabled = false`. Do not replace
the user's full configuration or remove unrelated marketplaces.

## Consumer validation

Run Flow and Router's `skills/<name>/scripts/validate_consumer.py` with separate
external scratch directories. Router's updated fixture requires exact 7.0.0.
Protobuf's reviewed reissued release is checked with:

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

Merge Router's source update, verify its actual merge tree and CI, refresh the
central lock, and pass `--require-merged`. Finish the central PR, choose a plugin
tag and verify installation at the immutable revision before publication.
Visibility changes, merges, tags and release creation remain explicit actions.

An OpenAI directory submission is a separate review with additional presentation
requirements: [submission guide](https://developers.openai.com/plugins/deploy/submission).
This Git marketplace package does not claim official-directory approval.
