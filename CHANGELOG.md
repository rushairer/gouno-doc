# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Documentation

- Link English and Chinese entrypoints to the Blog-owned source-verified BFF/SSO architecture and clarify that dated release evidence is not a current production certification. Keep normative protocols in their implementation repositories.
- Record the 2026-11-12 ten-repository documentation hygiene review: consolidated two dual doc/docs trees, reclassified historical TODOs/proposals, removed obsolete placeholders and preserved signed release evidence.

### Added

- Preserve independent final-release receipts for Gosso v1.7.2, Admin v0.7.25 and Blog v1.6.0, including exact identities/digests, SBOM/provenance checks and explicit manual/Staging publication exceptions.

### Changed

- Update both compatibility matrices from actual published downstream artifacts; retain Core/Template v1.4.0, CLI v1.3.0, UI v0.4.9 and Agent Demo v0.3.0. Document patched Go 1.26.11/1.27.4 requirements without rewriting historical releases.

## [1.3.1] - 2026-11-05

### Added
- Add bilingual Architecture Profiles guidance for Flat Layered and Capability Module as project/template conventions.

### Changed
- Record the published Gosso v1.7.0 and independent Agent Demo v0.3.0 artifacts without attributing newer candidate compatibility tests to older Admin/Blog tags.
- Record the published Core v1.4.0 → Template v1.4.0 → CLI v1.3.0 chain with exact release SHAs and dual-series integration evidence in both compatibility matrices.
- Separate actually published Gosso, Admin, Blog and npm baselines from release candidates; remove the untagged Agent Demo v0.2.0 claim from the formal matrix.
- Require latest-patch selection in reusable Go 1.26.x / 1.27.x quality workflows; update pinned Actions and golangci-lint v2.15.0.
- Document dependency-ordered releases and immutable upstream verification.

## [1.3.0] - 2026-09-11

### Added

- Add documentation governance rules that preserve normative ownership, bilingual alignment, compatibility discipline, and historical CHANGELOG facts.
- Add bilingual Template Authoring guides covering minimal architecture-neutral templates, optional Codegen v1, the two-stage rendering model, inherited `AGENTS.md` contracts, rendered-project verification, reusable CI, and immutable template releases.

### Changed

- Align Getting Started, Project Templates, and Code Generation guides with the released Codegen v1 architecture: project templates own concrete generator policy and may omit Codegen entirely.
- Separate default `gouno-template` DDD/Gin conventions from Gouno Core requirements.
- Document the two-stage bootstrap/Codegen rendering model and the legacy reserved `templates/` path.
- Update the compatibility matrix for the released `gouno-cli v1.2.1` → `gouno-template v1.3.0` → `gouno v1.3.0` chain.

## [1.2.0] - 2026-08-24

### Added

- Add bilingual engineering, Go support, release, and compatibility standards for the Gouno repositories.
- Publish SHA-pinnable reusable workflows for Go module quality, rendered project-template quality, and Conventional PR titles.

### Changed

- Establish Go 1.25.0 as the shared minimum and Go 1.25.x/1.26.x as the required CI matrix.

## [1.1.0] - 2026-08-20

### Changed

- Replace Template Sets guide with [Project Templates](./project-templates.md) guide reflecting the simplified `gouno-cli new -t` workflow.
- Update Code Generation guide: default controller path is now `internal/controller/`; removed `--template-set` flag.
- Update Middleware guide: documented `SecurityHeaders`, RateLimiter with `maxVisitors`, CSRF protection, and OIDC RS256 token verifier (`auth`).
- Update Getting Started guide: updated CLI options (`--module`, `--template`, `--skip-tidy`) and streamlined build instructions.

## [1.0.0] - 2026-05-31

### Added

- Getting Started guide (English / Chinese).
- Code Generation guide (English / Chinese).
- Template Sets guide (English / Chinese).
- Configuration guide (English / Chinese).
- Middleware guide (English / Chinese).
