# Flow and Router follow-up — 2026-10-10 KST

The source branches advanced while this follow-up started. Their existing fixes
were reviewed and fast-forwarded without rewriting other work. The initial checks below
recorded a pending merge candidate; the 2026-10-11 update at the end records
the later Flow merge. Router remains pending.

## Canonical changes

- Flow [PR #63](https://github.com/InnoSquadCorp/InnoFlow/pull/63),
  `f696e36ca50930c00520831ca1d6f09f44f685bd`: static CI fetches full tag
  history, the API gate defaults to `STABLE_VERSION`, and negative controls
  reject missing baseline tags or shallow CI checkouts. Its canonical skill
  now validates published 6.0.2 at `1176de1`; support remains stable 6.0.x.
- Router [PR #70](https://github.com/InnoSquadCorp/InnoRouter/pull/70),
  `b82dc6aa7e4d96de24d7607e93e0218c17ffe587`: the native visionOS probe
  waits for both physical appearance and canonical state recovery. Store commits
  notify the waiter. A native fault-injection control restores the previous
  appearance-only condition and requires the original canonical-state failure,
  then runs the corrected allow/reject/cancel scenarios. Its timeout is unchanged.
  These added commits change the probe and CI, not the library's runtime source.
  The Router skill tree is unchanged.
- Stream [PR #14](https://github.com/InnoSquadCorp/InnoNetwork-Stream/pull/14)
  was independently merged at `7fb61ac2843c5742368cd4e640588b4c61b476c0`.
  Its 18 successful checks, merge timestamp and unchanged skill tree were read
  live; the central source record now uses that actual merge commit.

## Fresh checks

- Flow principle-gate selftests and CI-efficiency negative controls passed.
  Nine Flow and four Router consumer-validator regression tests passed.
- The copied Flow 6.0.2 consumer passed 11 tests with strict concurrency and
  warnings as errors. Manifest/lock, active graph, SwiftSyntax 604.0.0, exact
  checkout SHAs, checkout cleanliness and source hashes were verified. The
  public annotated 6.0.2 tag still peels to `1176de1`.
- All 30 central tests, six canonical tree comparisons and both Claude plugin
  formats passed. The original alpha.7 Flow prompts were archived unchanged;
  current prompts now refer to 6.0.2 and a separately verified future patch.

Codex CLI 0.162.0-alpha.17.2 implicitly selected the refreshed Flow skill from
an isolated six-skill installation. Its read-only answer distinguished 6.0.x
support, exact 6.0.2 evidence and an unverified future 6.0.3. This is fresh
selection/version-policy evidence, not a new generation test; the 11 tests above
are the authored fixture. The initial PATH CLI 0.142.5 attempt failed before a
model response, then the bundled CLI passed. [Sanitized record](host-evaluation-flow-6.0.2.json).

The full Flow release preflight was not run locally. Router's native visionOS
regression is wired into its platform CI; it has not yet completed on this head.
Local validator tests do not replace that native execution.

## Initial merge gate — 2026-10-10

At the recorded check, Flow had 20 queued macOS jobs and Router had 25. The
jobs had no assigned runner. Flow's static principle gate passed, but neither
source PR had completed all selected checks. No check was waived and neither
PR was merged by this follow-up. See the exact-head
[status snapshot](release-status-1.0.0.json).

After each PR passes its required and selected validation, merge that exact
head, record the actual merge commit and compare the complete canonical skill
tree again. Then update the central lock and run central validation/CI. Until
then, Flow and Router remain `pull_request`; DI is also pending. The normal
merged-source package gate must continue to reject the candidate. No library
tag, plugin 1.0.0 release or visibility change is performed here.


## Flow merged — 2026-10-11 KST

Flow's exact head `f696e36` completed its real validation
[run 38041337882](https://github.com/InnoSquadCorp/InnoFlow/actions/runs/38041337882).
The metadata-only confirmation had previously exhausted its 21,000-second wait;
its second attempt then
[passed](https://github.com/InnoSquadCorp/InnoFlow/actions/runs/38041569412).
Both required contexts and all selected validation were successful before the
head-matched normal squash merge. No gate or timeout was relaxed.

PR #63 merged at `2026-10-10T18:17:52Z` to
`6b7c632500526cd87ab76e1d845d1b082327703e`. The merge's Flow skill tree is
`491a78f01d6e6540182d6ad8e2ee7ff0a43f9e6d`, identical to the reviewed central
snapshot. The source record now uses this actual merge commit; the public 6.0.2
API baseline and 6.0.x support range are unchanged. Post-merge main CI is separate
from the passing PR evidence.

A read-only status refresh also found that DI PR #59 had independently merged
at `2026-10-10T13:37:47Z` to `74a57b83664e431b45aa56f53286adeac86ccfb2`.
Its authoritative Git tree is unchanged at
`358bab55a293c1ec5d456c42a911a86fcbc90c03`. Only its central source record was
updated; this follow-up did not modify or merge DI.

Router PR #70 still has unfinished platform checks, including the native
visionOS regression. It is the only remaining `pull_request` source pin, so the
normal merged-source package gate still rejects the candidate. All six skill
contents are unchanged by this merge-record update; earlier consumer and host
results remain dated evidence rather than newly executed tests.
