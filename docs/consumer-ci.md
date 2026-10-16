# Exact Swift consumer CI

The bundle workflow runs all six library-owned consumer validators plus a
central-owned isolated Router 7.0.1 case on pull
requests, main pushes and version tags. Branch pushes retain the existing bundle
check without duplicating the seven PR consumer jobs. These checks resolve remote
dependencies, compile and test the isolated fixtures, then run an explicit
strict-concurrency build. They do not evaluate an AI host or publish a package.

For v1.0.0, [PR, merged-main and tag CI](release-verification-1.0.0.json) each
passed all seven cases and 83 Swift tests. The separate publication record
preserves exact dependency evidence, package checksums and public delivery checks.

## Runner and prerequisites

The hosted runner label is `xcode-27`, with
`DEVELOPER_DIR=/Applications/Xcode_27.0.app/Contents/Developer`.
The central runner requires Xcode 27.0, Apple Swift 6.4, macOS 27 and the macOS 27
SDK. This covers the SwiftSyntax 604 baseline and Stream's declared Swift 6.4 /
OS 27 boundary. The [official image inventory](https://github.com/actions/runner-images/blob/main/images/macos/xcode-27-arm64-Readme.md)
and [runner label announcement](https://github.com/actions/runner-images/issues/14404)
describe this preview image. Availability and installed versions are checked at
execution time; a missing/mismatched prerequisite fails the job. No older
toolchain, local dependency override or user Mac is used as a CI fallback.

Each matrix entry calls `scripts/validate_consumer_ci.py` with a fresh
`$RUNNER_TEMP/consumer-<label>` directory. That wrapper invokes the unchanged
`skills/<skill>/scripts/validate_consumer.py` using its own `swiftpm/` scratch
directory. Shared build/checkouts are not restored from a cache. The per-command
timeout records failure and kills the command's process group before collecting
artifacts; `fail-fast: false` lets the other consumers finish.

## Exact inputs

| Consumer | Version | Required library commit |
| --- | --- | --- |
| InnoDI | 7.0.0 | `4783eee7f674f99a337768c107b7a5f640810c2a` |
| InnoFlow | 6.0.2 | `1176de1e4783b638c03a9334f43cc49378957148` |
| InnoRouter | 7.0.0 | `33b0da7639105cfa8e6f5acffa3badb91b5e0254` |
| InnoRouter, central isolated case | 7.0.1 | `482587bcac8347857fd521ff38f169c010f48b83` |
| InnoNetwork | 6.1.0 | `79ff9f535a0a15ad8b52ce49cb5a4b1ea1dfec16` |
| InnoNetwork-Protobuf | Reissued 6.1.1 | `ba6ab8d6112d51efa69d92ac6739464bfc775aed` |
| InnoNetwork-Stream | 6.1.1 | `2af03b24cfc8f11442a3b9ba2fd8adcfe58d8116` |

Protobuf and Stream require exact Core 6.1.1 at
`44e4ca28c50c03f817231a077c0f3bdfdbc859c8`. All six fixtures pin SwiftSyntax
604.0.0 at `050f1a346fbbac0ca2cfb15a95274f7bd1cf0ccf`. Every transitive
version, revision and remote location is checked against the skill's support
record and lockfile, then the active graph/workspace and clean checkout HEADs.
The wrapper also rechecks final pins and clean checkout HEADs after its build.

Protobuf alone uses the existing documented release mode with annotated tag
object `eaea83c7f95f931b6e963c49ae10c7ef5f869438` and the reissued commit
above. Its validator checks the remote tag before and after testing and changes
only the isolated copy's adapter seed. All historical baseline fixtures remain
unchanged.

## Isolated Router 7.0.1 case

The Router skill source is the released 7.0.1 commit and exact tree
`645baccc66df3d8e7989787e875f7063939b6444`. Its upstream-owned support record,
manifest and lock still name the 7.0.0 baseline. The original six cases continue
to run with those historical inputs.

`--skill innorouter --case router-7.0.1` copies the entire skill to a separate
external directory. Only the temporary support record, `Package.swift` and
`Package.resolved` are adjusted to exact 7.0.1. Sources, Tests, instructions and
the original validator retain identical bytes and executable modes. Original and
adjusted input files and complete hash inventories are retained in the artifact.
The original validator performs its normal graph/checkout/test checks against
the temporary exact-release inputs. The central wrapper independently verifies
the reviewed lightweight tag before and after execution, checks an explicit
build, and rejects any change to the copied or original skill. This does not
rewrite the upstream baseline or promote historical evidence to a new run.

```bash
DEVELOPER_DIR=/Applications/Xcode_27.0.app/Contents/Developer \
python3 -B scripts/validate_consumer_ci.py --skill innorouter \
  --case router-7.0.1 --scratch-path /tmp/router-7.0.1-ci-fresh
```

## Evidence and limits

Every job uploads `consumer-<label>-<run-id>-<attempt>` for 14 days, including
on failure. The artifact contains the central report, toolchain output, source
pins/support record, original validator evidence and command logs, actual copied
manifest/lockfile, and SwiftPM workspace state when produced. Build caches and
dependency source trees are excluded. Partial evidence is retained when resolve
or build/test fails; a missing artifact is itself an error. A green bundle or
mocked Python test does not imply these Swift jobs passed.

On an authorized host meeting the prerequisites, use a fresh external path:

```bash
DEVELOPER_DIR=/Applications/Xcode_27.0.app/Contents/Developer \
python3 -B scripts/validate_consumer_ci.py \
  --skill innonetwork-protobuf --scratch-path /tmp/protobuf-ci-fresh
```

The tests cover each fixture's existing contracts. They do not establish
cross-library integration, minimum-OS/device behavior, FairPlay/background/audio
acceptance, model selection or generated-code quality. Preserve the separately
dated [host evaluations](host-support.md) and [publication checklist](release-1.0.0.md).
