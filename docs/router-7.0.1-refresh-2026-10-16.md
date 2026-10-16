# Router 7.0.1 source refresh

The [official Router 7.0.1 release](https://github.com/InnoSquadCorp/InnoRouter/releases/tag/7.0.1)
was published on 2026-10-16. Its reviewed lightweight tag resolves to
`482587bcac8347857fd521ff38f169c010f48b83`; the complete `skills/innorouter`
tree is `645baccc66df3d8e7989787e875f7063939b6444`.

Compared with the previous merged source `333ba03`, exactly two upstream files
changed: `references/support.json` and `references/testing-compatibility.md`.
They correct the SwiftSyntax lower bound from 603.0.0 to 603.0.2. Instructions,
Sources, Tests, fixture manifest/lock and the consumer validator are unchanged.
The complete source directory was copied and its bytes, paths and executable
modes checked against the immutable release checkout.

`sources.lock.json` records this released **skill source** separately from the
upstream-owned exact **library baseline**, which remains Router 7.0.0 at
`33b0da7639105cfa8e6f5acffa3badb91b5e0254`. The previous merged source and PR #70
are retained under `previous_source`; they are not presented as the 7.0.1 release.

The [central consumer CI](consumer-ci.md) preserves all six existing cases and
adds an isolated Router 7.0.1 case. Only temporary Package/support inputs change.
The unchanged validator, Sources and Tests execute against the exact reviewed
release, with tag identity checked before and after the run, exact dependency
and clean-checkout checks, strict-concurrency tests and an explicit build.
Artifacts retain original and adjusted inputs and their hashes. Run results are
recorded separately in PR/CI and release verification evidence.

Earlier [7.0.0/source follow-up evidence](flow-router-followup-2026-10-10.md)
remains historical. The new patch check does not qualify AI hosts, device/native
lifecycle, cross-library integration or other patches. Repository visibility
and the intended private audience remain unchanged.
