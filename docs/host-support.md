# Use the skills in other AI tools

alpha.13 added project installation and chat/API reference packs. alpha.14 fixes
consumer command diagnostics in all six skills; guidance and API fixtures are unchanged. A host adapter changes delivery,
not supported library versions or qualification status. These standard-library
tools require Python 3.9+.

## Delivery paths

| Host | Delivery | Selection | Qualification |
| --- | --- | --- | --- |
| Codex | Existing plugin or `.agents/skills/` | Native | Reused alpha.12 host evidence, unchanged guidance; helpers updated in alpha.14 |
| Claude Code | Existing plugin or `.claude/skills/` | Native | Reused alpha.12 host evidence, unchanged guidance; helpers updated in alpha.14 |
| Grok Build / CLI | `.grok/skills/` or Claude-compatible plugin | Native | Official format and local copy checks; CLI unavailable here |
| Grok web/app | Per-library Markdown attached or pasted | User chooses context | Export checked; live upload/model behavior unverified |
| Grok API | Selected context sent to xAI Responses | Explicit `--skill` | Offline request/response tests; no live key available |
| Gemini CLI | `.gemini/skills/` or `.agents/skills/` | Native on a skills-capable version | Local file installation checked |
| Cursor Agent | `.cursor/skills/` or `.agents/skills/` | Native | Local file installation checked |
| GitHub Copilot | `.github/skills/` or `.agents/skills/` | Native on a skills-capable version | Local file installation checked |
| Other text assistants, including ChatGPT/Gemini chat | Markdown attached or pasted | User chooses context | Text delivery, not a native plugin claim |

Paths follow official [Grok](https://docs.x.ai/build/features/skills-plugins-marketplaces),
[Gemini CLI](https://geminicli.com/docs/cli/skills/),
[Cursor](https://cursor.com/help/customization/skills) and
[Copilot](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills)
documentation checked on 2026-10-10. Grok documents reuse of Claude marketplaces
and plugins. This does not establish plugin installation in Grok web/app.

## Project installation

Clone the reviewed branch using [distribution](distribution.md), then:

```bash
python3 scripts/portable_skills.py install --host grok --project /path/to/app --dry-run
python3 scripts/portable_skills.py install --host grok --project /path/to/app
python3 scripts/portable_skills.py install --host gemini --project /path/to/app --skill innodi --skill innoflow
```

`--host` accepts `grok`, `gemini`, `cursor`, `copilot`, `codex`, `claude`, or
`agents` (the common `.agents/skills` directory). The project must exist.
Identical installations are a no-op; different existing skills or symlink paths
cause an error before copying. The installer preserves resources, notices and
executable bits, and does not change host configuration, credentials or AGENTS.md.
Do not run concurrent installers against the same destination.

Restart the host and inspect its skill list. Grok CLI provides `/skills` and
explicit invocation such as `/innodi`. Automatic selection depends on the host
and task. Use a skills-capable host version; file-copy success alone does not prove
discovery. Avoid duplicate standalone/plugin copies of the same skill.

## Grok web/app and other chats

```bash
python3 scripts/portable_skills.py export --output artifacts/portable-alpha.14
```

This creates `START_HERE.md`, a catalog, six per-library Markdown files,
`innosquad-skills.zip`, and SHA-256 checksums. Add `--skill innodi` to select one
library. Choose a new output path for each export; previous packs are preserved.
Each Markdown file includes instructions, version records, references, examples,
scripts and notices as labeled file sections. Relative paths refer to those sections.

Attach the relevant `.md` file where your Grok web/app offers attachment, or paste
the relevant sections into the chat. Include the project manifest, lockfile and
code needed for the task. Ask Grok to state the baseline it read before generating
code. Attachment UI and context limits depend on the account/host and were not
verified here. The same text works as supplied reference context in other chats.

The ZIP preserves native skill folders for file-based agents; uploading it is
not web-chat plugin installation. Supplied scripts are reference text unless a
host actually has the tools and authorization to run them. A chat cannot claim
Swift compilation or device validation merely because it read this pack.

## Grok API

The client uses xAI's preferred [Responses API](https://docs.x.ai/developers/model-capabilities/text/generate-text)
and its [request/response format](https://docs.x.ai/developers/rest-api-reference/inference/responses).
Set `GROK_MODEL` to a Responses-compatible model available to your account.
Create `task.txt` containing the task and project context you intend to send.

```bash
# Inspect the request without an API key or network call.
python3 scripts/grok_request.py --skill innodi --model "$GROK_MODEL" \
  --prompt-file task.txt --dry-run > request.json

# Set XAI_API_KEY through your local secret-management mechanism first.
# This command makes one billable xAI API request.
python3 scripts/grok_request.py --skill innodi --model "$GROK_MODEL" \
  --prompt-file task.txt --timeout 120 --max-output-tokens 4096 > answer.json
```

Repeat `--skill` only for relevant libraries. The client sends selected references
and that prompt file; it does not scan a project or execute local tools. It uses
`store: false`, a bounded response size and timeout, no redirects and no automatic
retries. HTTP/network errors and incomplete or malformed responses exit nonzero.
Timeout delivery may be uncertain; inspect account usage before retrying.
Keys are read only from `XAI_API_KEY`, never included in dry runs or error output.
Request/answer files still contain your task data: keep them out of source control.
Generated code requires validation in the actual consumer environment.

## Validation and outstanding release work

`python3 -B -m unittest discover -s tests -v` covers original file/mode identity
for every target host, repeat installs, collision/symlink refusal, deterministic
selected-only exports, notices, dry runs, API request/response parsing and failure
behavior. CI does not call remote models or billable APIs.

Grok runtime behavior is unverified: the CLI is unavailable and `XAI_API_KEY` is
absent here. Other hosts' actual selection/generation is separate from the local
installation tests. Existing alpha.12 evidence remains dated.
One Copilot CLI 1.0.11 read-only probe stopped before model use because its
configured `gpt-5-mini` model was rejected by the server (HTTP 400, unsupported
model); it is not a passed skill-selection case. Gemini CLI 0.24.0 and Cursor
Agent 2026.01.02 were inventoried but not used for fresh model evaluation.
See [portable validation evidence](portable-validation-alpha.13.json).

The graph-output defect is fixed in all six alpha.14 snapshots; see the
[correction report](consumer-output-fix-alpha.14.md). Five owning-library PRs
still await merge. Router's earlier merge CI performance failure and Stream's
unpublished 6.1.1 baseline remain separate release conditions. Public publication and official
directory submission are separate actions.
