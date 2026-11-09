# LightCraft TH 0.19.0-th.1 preparation

Base: complete upstream v0.19.0 tag at `16636c45a63bff3065a6fd31aecc22a6fc15ca53`. Upstream application source and its history are retained; external dependency revisions are unchanged.

The Thai interface currently contains 3,844 plain catalog entries and 336 format entries. Technical names and user data retain their original forms. Draft translations combine existing shared Thai text and machine-assisted drafts with terminology, numeric-value and code-identifier corrections. This is not a claim of independent linguistic review of every sentence.

Static checks cover every reference-catalog key, the upstream non-test literal scanner, Rust formatting signatures, fixed numeric values and code identifiers. The compiled localization report, complete source CI, native package checks and screenshots must still pass before publication.

New desktop profiles default to Thai; saved language choices remain respected. The Thai update origin is the independent repository. Thai prereleases require manual downloads from Releases. The Mac package includes `lightcraft-cli` for MCP; headless `mcp --demo` operates on a synthetic in-memory library.

No new Thai release or platform validation is claimed by this preparation note. Final platform provenance and limitations will be recorded in the release validation report.
