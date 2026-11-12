# Gouno ecosystem documentation hygiene — 2026-11-12

> **Scope:** Read-only inventory followed by documentation-only changes on selected `main` branches. Reviewed `AGENTS.md` before edits. Source code, live router/configuration and formal published releases take priority over README claims and old TODO cards. **This is not a CI, deployment, security or manual visual certification.**

## Results by repository

| Repository | Checked-main documentation result | Resulting main SHA |
| --- | --- | --- |
| [gouno-blog](https://github.com/rushairer/gouno-blog) | Merged lone `doc/release-manifest-v1.6.0.md` into `docs/releases/`; updated CHANGELOG/checklist/candidate-review links and clarified v1.6.0 published vs dated candidate state. Added canonical docs index; marked 2026-09 quality/UI plans historical, removed **nine empty `planned/unexecuted` UI-task placeholders** (recoverable in Git history), preserved release receipts, BFF ADR and UI certification evidence. | `90ba5fb6` |
| [gosso](https://github.com/rushairer/gosso) | Moved all **17** maintained `doc/*` files into `docs/` (ADR, architecture invariants, operator/integrator guides); updated README languages, AGENTS, CONTRIBUTING, CODEOWNERS, PR template, architecture check, ignore rules and internal Account README. Generated `docs/openapi.yaml`/Swagger stay fixed. Added docs index. | `52e9e977` |
| [gosso-admin](https://github.com/rushairer/gosso-admin) | Updated roadmap to distinguish published v0.7.25 from unverified operational gates; marked November 8–9 local Gosso v1.7.1 patches as historical/superseded by formal v1.7.1/v1.7.2. Preserved patch checksums and independent acceptance evidence, added docs index. | `0058597c` |
| [gouno-ui](https://github.com/rushairer/gouno-ui) | Moved resolved “open defects” ledger into `docs/history/foundation-integrity-closed-defects-2026-09.md` and linked it from the completed Foundation program. Added docs index separating living design/API and certification contracts from completed audits/proposals. | `15284fe9` |
| [gouno-template](https://github.com/rushairer/gouno-template) | Deleted empty `doc/.gitkeep` placeholder and introduced `docs/README.md` as the single documentation folder in newly scaffolded projects. | `c528022b` |
| [gouno](https://github.com/rushairer/gouno) | Added docs index separating normative Codegen v1 schema from dated security/release snapshots. | `9c246a1e` |
| [gouno-doc](https://github.com/rushairer/gouno-doc) | Added paired English/Chinese entrypoint references to the Blog-owned As-Is SVG and this hygiene record, without duplicating protocol contracts; historical compatibility data remains versioned. | This report's commit |
| [gouno-cli](https://github.com/rushairer/gouno-cli) | Reviewed; single `docs/project-template-contract.md` is the normative bootstrap contract, no `doc/docs` duplication or demonstrated current-state defect requiring modification. | `a3930d13` |
| [gosso-client](https://github.com/rushairer/gosso-client) | Reviewed; no parallel documentation directories. Current README distinguishes confidential BFF versus ordinary SPA, `package.json` declares `0.9.3`, CHANGELOG tracks `0.9.3`. No additional duplicate index was created. | `8a0eefd5` |
| [gouno-agent-demo](https://github.com/rushairer/gouno-agent-demo) | Reviewed; has one `doc/openapi.yaml` only, **not two competing trees**. Left generated/API paths unchanged rather than risk a runtime or tooling path migration without evidence. | `735794f1` |

## What was removed — and what was preserved

1. **Removed:** the obsolete `gouno-blog/doc/` path after moving its historical release manifest, the obsolete `gosso/doc/` tree after moving all authored guides, the template's empty `doc/.gitkeep`, Gouno UI's misleading “open defects” path after preserving the resolved record, and nine old Blog UI-phase task placeholders with no execution evidence.
2. **Preserved:** historical CHANGELOG entries, ADRs, security/DB migration reports, released version manifests, exact image digests/signatures/SBOM/provenance receipts, UI certification ledgers and actual regression-test reports. Historical paths retained in immutable JSON inventories are not automatically renamed, because those JSON values describe the old git revision.
3. **Corrected status:** Blog v1.6.0, Gosso v1.7.2, Gosso Admin v0.7.25 and the Core/CLI/Template release chain have published GitHub releases; earlier candidate and TODO records are dated observations, not today's rollout checklist. **Publication does not prove manual UI certification, external Staging, rollback exercises or production deployment**.

## Verification scope

- Confirmed remote `main` tree layout after commits: neither `gouno-blog` nor `gosso` retains a `doc/` tree; `gouno-template` no longer has its empty placeholder.
- Fetched current files and checked locally resolving relative Markdown links in the **selected current entrypoints and migration targets** for Blog, GOSSO, GOSSO Admin, Gouno UI and Template; no missing relative target was found in that scoped sample.
- No production source code or CI definitions were modified. No build, full site link crawler, end-to-end login, browser visual review, runtime execution, or production deployment verification was performed as part of this docs-only audit.

## Follow-up rules

- Before removing more dated files, prove duplication or invalidity against current code and inbound links. **Small historical records with unique evidence are not redundant just because their task is closed.**
- Keep one current docs index per substantial docs tree, not a new top-level index for single-file or no-doc repositories.
- When implementation changes, update the owning README, exact-version compatibility matrix and current docs **in the same code change**. Keep historical evidence and CHANGELOG history as immutable release narratives.
- Ensure any future `gosso` or `gouno-template` source changes pass their normal CI/rendered-project checks; this static documentation review cannot certify codegen or deployment behavior.
