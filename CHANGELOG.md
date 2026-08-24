# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [1.2.1] - 2026-08-24

### Fixed

- Correct the immutable `golangci-lint-action` SHA in the reusable Go module quality workflow.

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
