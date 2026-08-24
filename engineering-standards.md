# Gouno Engineering Standards

## Releases and compatibility

- Every repository uses independent Semantic Versioning and a hand-curated
  Keep a Changelog file with an `Unreleased` section.
- Tags, package versions, image versions, API documentation, and migration
  notes must describe the same release. Published tags are immutable.
- Go projects support the latest security patch of the current and previous
  stable Go series. A minor release may raise the minimum Go version when the
  changelog and README state the impact.

## Configuration and APIs

- Environment variables use an owning subsystem prefix such as `GOUNO_`,
  `GOSSO_`, or `BLOG_`; production secrets are required and have no defaults.
- Credentialed CORS uses exact HTTPS origins. Browser authentication defaults
  to server-set HttpOnly cookies with CSRF protection.
- JSON errors expose a stable machine code, safe message, request identifier,
  and HTTP status. Internal errors and secrets remain in structured logs only.
- Logs use structured fields including timestamp, level, service, version,
  request ID, event, and outcome. Tokens, cookies, passwords, DSNs, and private
  personal data are always redacted.

## Quality and supply chain

- Commits follow Conventional Commits. CI actions are pinned to full commit
  SHAs with least-privilege permissions.
- Go gates: gofmt, tests, race detector, vet, golangci-lint, and govulncheck.
  Node gates: Prettier, lint, typecheck, coverage, build, and npm audit.
- Production images and deployment dependencies use semantic versions plus
  digests. Releases include SBOM, provenance, and a verifiable signature.
- Each repository includes LICENSE, README, CHANGELOG, SECURITY,
  CONTRIBUTING, CODE_OF_CONDUCT, SUPPORT, and RELEASE_CHECKLIST.

## Pull-request acceptance

A pull request cannot merge while a reachable vulnerability, secret finding,
failing compatibility test, mutable production dependency, or undocumented
public contract change remains unresolved.
