# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

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
