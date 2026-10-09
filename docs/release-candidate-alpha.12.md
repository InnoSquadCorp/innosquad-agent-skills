# alpha.12 validation — 2026-10-09

This candidate refreshes Flow/Protobuf released snapshots, qualifies Router 7.0.0
through source PR #69, uses the `innosquad` marketplace identity and licenses
original distribution material under MIT.

Fresh consumer tests: Flow 11, Router 11 and reissued Protobuf 14 passed with
complete strict concurrency and warnings as errors, with exact remote graph
verification. Router wrong-SHA and missing-version controls rejected before Swift.

Bundle validation and six controls passed. Claude catalog/manifest validation
passed without warnings. alpha.12 installation and host results are pending.

The earlier alpha.11 Stream run after Claude reauthentication is reused evidence:
implicit selection and generated consumer passed 5 independent strict tests,
including 13 parameterized invalid settings. It did not exercise live media.
Earlier Codex reports remain dated evidence for unchanged instructions.

Public plugin publication, Router source merge and directory listing have not
been performed. These are separate from local validation.
