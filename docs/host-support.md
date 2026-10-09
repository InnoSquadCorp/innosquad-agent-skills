# Use the skills in other AI tools

The 1.0.0 preparation candidate preserves alpha.14 skill trees and library support
ranges. Host delivery and model qualification are separate. The installer and
packaging tools use Python 3.9+ and do not change host settings or authentication.

## Delivery paths

| Host | Delivery | Selection | Qualification |
| --- | --- | --- | --- |
| Codex | Existing plugin or `.agents/skills/` | Native | Dated alpha.12 native evidence; fresh alpha.14 standalone DI selection and 4 tests passed |
| Claude Code | Existing plugin or `.claude/skills/` | Native | Dated alpha.12 generation passed; fresh alpha.14 catalog recognized, OAuth expired |
| Grok Build / CLI | `.grok/skills/` or Claude-compatible plugin | Native | Official format and local copy checks; CLI unavailable here |
| Grok web/app | Per-library Markdown attached or pasted | User chooses context | Export checked; live upload/model behavior unverified |
| Grok API | Selected context sent to xAI Responses | Explicit `--skill` | Offline request/response tests; no live key available |
| Gemini CLI | `.gemini/skills/` or `.agents/skills/` | Version-dependent feature flag | 0.24.0 discovered all six with the flag enabled; generation blocked by sign-in |
| Cursor Agent | `.cursor/skills/` or `.agents/skills/` | Native loader present | Files/installed loader checked; actual discovery and generation blocked by authentication |
| GitHub Copilot | `.github/skills/` or `.agents/skills/` | Native catalog and explicit invocation | Six discovered; CLI 1.0.11 + GPT-4.1 implicit selection and generated-code evaluation failed |
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

## Gemini CLI setup

On the evaluated **0.24.0** installation, Agent Skills is experimental and disabled
by default. Merge this field into the project's existing `.gemini/settings.json`;
preserve all other keys:

```json
{"experimental":{"skills":true}}
```

Restart Gemini and run `gemini skills list`. All six Inno skills were discovered
with this setting. The installer returns this guidance but never writes settings.
Check the requirements of your installed version; newer versions may differ.
Finish Gemini's sign-in before testing a request. The recorded probe stopped at
OAuth sign-in, so discovery does not establish model behavior.

## Copilot usage and current limit

In CLI **1.0.11**, use `/skills` to verify the six project entries. An explicit
request such as “Use the innodi skill, inspect my Package.resolved, then implement
the override and tests” successfully invoked `skill innodi` and read references.

**GPT-4.1 is not generation-qualified by this evaluation.** It skipped the skill
on the implicit request and generated an incompatible runtime registration API.
Explicit activation loaded the correct material but still generated a container
inside a test function, which failed compilation. Both were read-only, first-answer
probes; a full build-and-repair agent loop was not evaluated. Compile generated
code in the consumer and do not infer correctness from successful activation.
The installed model menu also listed models that the server rejected. Verify an
actual request before treating a model as available; the installer does not select
or change your model. See [the recorded evaluation](host-evaluation-non-grok.md).

## Grok web/app and other chats

```bash
python3 scripts/portable_skills.py export --output artifacts/portable-1.0.0-candidate
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

Grok runtime behavior remains unverified: no CLI or live API execution was
available in the recorded review. The latest non-Grok evidence is in the
[host evaluation](host-evaluation-non-grok.md); older
[alpha.12](release-candidate-alpha.12.md) and [portable checks](portable-validation-alpha.13.json)
remain dated records. Authentication-blocked hosts need a new successful request
before their qualification status can change.

All six validator fixes are preserved. The [1.0.0 preparation checklist](release-1.0.0.md)
tracks source merges, exact-commit checks, Stream's preview status and publication.
The helper correction details remain in the [alpha.14 report](consumer-output-fix-alpha.14.md).
