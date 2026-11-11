# Gouno Ecosystem 1.4 release closeout — 2026-11-11

**Publication Complete: YES, under the explicit maintainer publication exception. Original all-gates Release Complete: NO.** Gosso v1.7.2, GOSSO Admin v0.7.25 and Gouno Blog v1.6.0 are formal releases with annotated tags, successful final-source workflows, versioned multi-architecture images and separate independent artifact verification. Manual Showcase certification and external Staging remain unverified; no production deployment occurred. This report records that distinction instead of converting waived work into passed checks.

## Authorization and completion states

The requesting maintainer directed: “你去线上 ssh root@io84.com 目测一下吧。其他都默认通过。强行发版吧。” The explicit one-release exceptions are committed in [Admin](https://github.com/rushairer/gosso-admin/blob/v0.7.25/docs/quality/release-exception-2026-11-11.md) and [Blog](https://github.com/rushairer/gouno-blog/blob/v1.6.0/docs/quality/release-exception-2026-11-11.md). GitHub-enforced merge rules, actual automated tests, scanner thresholds and signature validation remained in force. No approval or human identity was fabricated.

| State | Gosso v1.7.2 | Admin v0.7.25 | Blog v1.6.0 |
| --- | --- | --- | --- |
| Code Ready | Yes | Yes | Yes |
| CI Ready (accepted tag source) | Yes | Yes | Yes |
| Manual Certification Ready | Not applicable to backend | No; pending, publication exception | No; pending, publication exception |
| Staging Ready | Not independently established | No; publication exception | No; publication exception |
| Release Published | Yes; independently verified | Yes; independently verified | Yes; independently verified |
| Production Deployed by this closeout | No | No | No |

## Formal versions, main and immutable tags

Core v1.4.0, Template v1.4.0, CLI v1.3.0, UI v0.4.9, Doc v1.3.1 and Agent Demo v0.3.0 were retained and rechecked read-only. Gosso v1.7.0 first advanced to1.7.1 for persisted Client Secret rotation and concurrency repairs, then1.7.2 for the newly published Go HTTP race advisory. Admin advances0.7.24→0.7.25; Blog advances1.5.26→1.6.0. No existing tag was recreated or overwritten; no UI v0.4.10 was manufactured.

| Repository | Formal version / GitHub Release | Main SHA at audit snapshot | Tag commit SHA |
| --- | --- | --- | --- |
| gouno | [v1.4.0](https://github.com/rushairer/gouno/releases/tag/v1.4.0) | `13d4a0adc4b6cf343c709019159b8609ab4b5875` | `20efba0af181cb3e03c5bcb199576bfcdec1bd7f` |
| gouno-template | [v1.4.0](https://github.com/rushairer/gouno-template/releases/tag/v1.4.0) | `01f227f34f6c056998a006bb8320f6187822aaf4` | `9f0cba9c8a6be6331f48596c83663efbec5490a2` |
| gouno-cli | [v1.3.0](https://github.com/rushairer/gouno-cli/releases/tag/v1.3.0) | `a3930d1391ce3aedb8661eef472555611fd54540` | `087c00a523a6ec8c512d5eb9c65f657f6be8d5fb` |
| gosso | [v1.7.2](https://github.com/rushairer/gosso/releases/tag/v1.7.2) | `95fde424eff854e12d95d73a00526b11ea186339` | `95fde424eff854e12d95d73a00526b11ea186339` |
| gosso-admin | [v0.7.25](https://github.com/rushairer/gosso-admin/releases/tag/v0.7.25) | `364eee6c244dc380a9e96b2c015513fab3ae4760` | `4545495bcdc518af65cc6c15a9695b9ef5df5e19` |
| gouno-blog | [v1.6.0](https://github.com/rushairer/gouno-blog/releases/tag/v1.6.0) | `c945ad804f206728f66d86dce8d290855ce11050` | `0e8c527dcae40f931898930483fb24a00a840232` |
| gouno-ui | [v0.4.9](https://github.com/rushairer/gouno-ui/releases/tag/v0.4.9) | `ad29789e3583200deae486dc301d8c06b9c8ce2a` | `4495147ae0b9807d2e5c9137187cfdc3e906cceb` |
| gouno-doc | [v1.3.1](https://github.com/rushairer/gouno-doc/releases/tag/v1.3.1) | `db1ffc4d2ea933f74f18308a21f0561907114bb7` | `fad499f7f28ff2e86d03d5c26ae6de127222d915` |
| gouno-agent-demo | [v0.3.0](https://github.com/rushairer/gouno-agent-demo/releases/tag/v0.3.0) | `735794f1982a0f969e5b956a929f5e9a92440e86` | `ca372fc72379dbf63e6794f5d4e65af7c88e8ba7` |

The main column is a snapshot before committing this report, not a self-referential claim about its future merge SHA. Post-publication evidence commits may advance application main without moving a validated release tag. The tag column identifies the actual tested release source. Documentation compatibility updates land after Doc v1.3.1; that older tag was not republished. [Machine-readable refs](release-evidence-2026-11-11/ecosystem-published-state.json) include annotated tag-object SHAs.

## Exact-source CI and security evidence

Every listed application workflow is completed/success for the exact tag source; publication and independent verification are separate runs.

| Project | Accepted source | Final source checks | Publication and separate verification |
| --- | --- | --- | --- |
| gosso | `95fde424eff854e12d95d73a00526b11ea186339` | [CI](https://github.com/rushairer/gosso/actions/runs/42991114015), [Images](https://github.com/rushairer/gosso/actions/runs/42991113984) | [Tagged publisher](https://github.com/rushairer/gosso/actions/runs/42993412418); [independent acceptance](https://github.com/rushairer/gouno-doc/actions/runs/42996028182) |
| gosso-admin | `4545495bcdc518af65cc6c15a9695b9ef5df5e19` | [Gosso Showcase Parity](https://github.com/rushairer/gosso-admin/actions/runs/42996219892), [UI Browser Acceptance](https://github.com/rushairer/gosso-admin/actions/runs/42996213474), [CI](https://github.com/rushairer/gosso-admin/actions/runs/42996206473), [Gosso Release Compatibility](https://github.com/rushairer/gosso-admin/actions/runs/42996206636), [Images](https://github.com/rushairer/gosso-admin/actions/runs/42996206685), [Security](https://github.com/rushairer/gosso-admin/actions/runs/42996206593) | [Tagged publisher](https://github.com/rushairer/gosso-admin/actions/runs/42996686038); [independent acceptance](https://github.com/rushairer/gouno-doc/actions/runs/42997051605) |
| gouno-blog | `0e8c527dcae40f931898930483fb24a00a840232` | [Blog Showcase Parity](https://github.com/rushairer/gouno-blog/actions/runs/42997883601), [UI Browser Acceptance](https://github.com/rushairer/gouno-blog/actions/runs/42997872284), [Gosso Release BFF Compatibility](https://github.com/rushairer/gouno-blog/actions/runs/42997862192), [CI](https://github.com/rushairer/gouno-blog/actions/runs/42997862051), [Publish Images](https://github.com/rushairer/gouno-blog/actions/runs/42997862088) | [Tagged publisher](https://github.com/rushairer/gouno-blog/actions/runs/42999093507); [independent acceptance](https://github.com/rushairer/gouno-doc/actions/runs/42999630031) |

Admin PR99 and Blog PR425 also pass their PR-only dependency reviews and image checks. A dependency-review job event-skipped on main is not represented as a fresh PR review. The existing frontend format/lint/typecheck/test/coverage/build, Go race/vet/govulncheck, required PostgreSQL integration/Seed, BFF, container scans and image contracts were retained. Browser/parity workflows prove their automated scope, not human certification. Historical foundation release workflows and current-main metadata are preserved in [the foundation audit](release-evidence-2026-11-11/foundation-audit.json); those unchanged artifacts were not rebuilt in this closeout.

Fresh Blog govulncheck initially failed on [GO-2026-6859](https://pkg.go.dev/vuln/GO-2026-6859), an HTTP/1 MaxBytesReader header race. Gosso and Admin Seed now use immutable Go 1.27.4 builders and a Go 1.26.11 module floor; Blog Backend/Seed use Go 1.27.4 with a fail-closed patch floor. Actual published Go SBOM components confirm1.27.4. This is a minimal security rebuild, with Core v1.4.0 and API/business boundaries retained. Earlier Go 1.27.3 success is historical, not current advisory clearance. Existing musl/zlib, x/net, JOSE/Tink, dependency and coverage floors were not lowered.

## Published compatibility and registries

| Consumer | Published dependency / accepted relationship |
| --- | --- |
| Template v1.4.0 | Core v1.4.0; default template owns its architecture/Codegen choices |
| CLI v1.3.0 | Live-default and pinned Template v1.4.0 Bootstrap; verbatim Codegen assets |
| Gosso v1.7.2 | Core v1.4.0; public Go Proxy exact source and Helm OCI1.7.2 accepted |
| Admin v0.7.25 | Actual signed Gosso v1.7.2 digest; global cross-owner governance, retired/replacement Client Secret authentication and privilege/session boundaries exercised |
| Blog v1.6.0 | Independent BFF acceptance against actual signed Gosso v1.7.2; verified Admin v0.7.25 frontend/Seed production references; Core v1.4.0 |
| Both frontends | Exact @gouno/ui 0.4.9 and @gosso/client 0.9.3; Node 24 LTS >=24.15 and <25 |
| Agent Demo v0.3.0 | Retained published Core v1.4.0 / dual-series Go baseline; independent earlier release |

Public module baselines remain `github.com/rushairer/gouno@v1.4.0` and `github.com/rushairer/gouno-cli@v1.3.0`. Fresh independent Gosso verification resolves `github.com/rushairer/gosso@v1.7.2` through the public Proxy and checks Origin.Hash equals `95fde424eff854e12d95d73a00526b11ea186339`. Template root go.mod is a Bootstrap template, not a publishable module. Admin and Blog application images are not new npm package publications.

Both npm tarballs were independently downloaded and hashed on November 9; current accepted release locks still match those exact registry SHA512 integrity values, and final CI runs npm installation/quality gates. [Integrity receipt](release-evidence-2026-11-11/npm-integrity.json) retains checksums and dates. npm signature/provenance cryptographic verification is not claimed.

## Immutable image, signature, SBOM and provenance results

| Image | Actual immutable reference | Exact-identity Cosign verification | Other independent acceptance |
| --- | --- | --- | --- |
| gosso / gosso | `ghcr.io/rushairer/gosso@sha256:bf398c6c2129da2f68c030dece3ceb52f8f5a7a6036a58b797c8e3f0619b5e90` | Verified | SPDX + CycloneDX; amd64 + arm64 |
| gosso-admin / frontend | `ghcr.io/rushairer/gosso-admin-frontend@sha256:955792f63712298b8d588ff2b2eceb66d1b110ea8e919bb2dd392eb4800b160c` | Verified | SPDX + CycloneDX; amd64 + arm64 |
| gosso-admin / frontend-identity-admin | `ghcr.io/rushairer/gosso-admin-frontend-identity-admin@sha256:36a9191a4128b80d48eb84f7c3ec02f74abc584c0d976dbe7d5d7ac45d412984` | Verified | SPDX + CycloneDX; amd64 + arm64 |
| gosso-admin / seed | `ghcr.io/rushairer/gosso-admin-seed@sha256:ca6f1624c0908e9221ba98da5cb991d60c0b1f4702b5369131a885fda1c23eca` | Verified | SPDX + CycloneDX; amd64 + arm64 |
| gouno-blog / backend | `ghcr.io/rushairer/gouno-blog-backend@sha256:40db53e72d8eef94848fd4b8d1b335265b3c2ca4c0f7c8e105c05a146418dcab` | Verified | SPDX + CycloneDX; amd64 + arm64 |
| gouno-blog / frontend | `ghcr.io/rushairer/gouno-blog-frontend@sha256:7896ed1fdf16a3df2c58c5ebc76f580b39b2fc34d8eaae9fa585dae8fc52af1c` | Verified | SPDX + CycloneDX; amd64 + arm64 |
| gouno-blog / seed | `ghcr.io/rushairer/gouno-blog-seed@sha256:278195d6fe9b0af79b036f78f30cc2f3fb776eb02ba47b69145fa4350fc86daa` | Verified | SPDX + CycloneDX; amd64 + arm64 |

All signatures are verified against immutable image@digest, issuer `https://token.actions.githubusercontent.com`, and exactly:

- Gosso: `https://github.com/rushairer/gosso/.github/workflows/release.yml@refs/tags/v1.7.2`.
- Admin: `https://github.com/rushairer/gosso-admin/.github/workflows/images.yml@refs/tags/v0.7.25`.
- Blog: `https://github.com/rushairer/gouno-blog/.github/workflows/publish-images.yml@refs/tags/v1.6.0`.

Independent receipts verify version tag resolution, OCI content hashes, release attachment hashes/formats, both architectures, exact declared source SHA and post-publication signature validity. Gosso additionally verifies its signed CycloneDX attestation subject/predicate against the Release attachment, Helm chart/appVersion1.7.2 with OCI content hashes, and public Go Proxy origin. BuildKit local-directory provenance cross-checks declared VCS metadata and root request arguments (plus OCI labels for Admin/Blog); it is not claimed to be a Git material content-hash or hermetic-build proof. A successful signing step alone was never treated as successful verification.

Permanent receipts: [Gosso](release-evidence-2026-11-11/gosso-independent-verification.json), [Admin](release-evidence-2026-11-11/admin-independent-verification.json), [Blog](release-evidence-2026-11-11/blog-independent-verification.json). Complete raw verifier artifacts remain attached to their linked Actions runs (90-day retention); source checks and checksums are preserved here. Blog's [completed release manifest](https://github.com/rushairer/gouno-blog/blob/main/doc/release-manifest-v1.6.0.md) records the real three-image digests in a post-publication commit; the release tag remains immutable.

## Showcase, online observation and Staging boundaries

Admin `docs/ui/showcase-parity-certifications.json` and Blog `docs/ui-redesign/showcase-parity-certifications.json` remain needs-manual-recertification, including blog-admin-ai. Existing Canonical/UI ownership and package pins remain intact. No certification row is promoted from automated CI.

Read-only SSH access to root@io84.com succeeded. Host-local operational constraints were read; unrelated services, private routes, secrets and deployment configuration were preserved. Login/readiness/home/health returned HTTP200. After native browser acquisition failed, regular Playwright Chromium used a read-only SSH SOCKS tunnel to inspect the actual public login and Blog: desktop/mobile, settled content, theme switch, mobile drawer, scrolling/footer and keyboard focus. Saved screenshots were actually viewed; observed pages had no uncaught JavaScript errors or horizontal overflow in this limited scope. [Sanitized receipt and screenshot hashes](release-evidence-2026-11-11/production-public-render-review.json). Initial transient loading captures were not counted as completed acceptance.

The online installation used older floating-main images (observed Admin 51fe7448 and Blog 0aee8208); this is not authenticated candidate review, Staging, release-image deployment acceptance or production promotion. No production account mutation, secret retrieval, service restart, container replacement or deployment was performed. The temporary SSH tunnel was closed.

## Remaining exceptions and reproducibility

No automated publication blocker remains for the three verified releases. The deferred work is real maintainer Showcase certification, named external Staging preflight, target-specific TLS/MFA/SMTP and secret/operator acceptance, historical-data upgrade/recovery/rollback and a separately authorized production promotion. Earlier disposable local PostgreSQL recovery remains evidence of its own scope, not completion of target Staging. These statuses remain unverified under the explicit owner exception. Full original all-gates operational closeout must not be claimed until those actual receipts exist.

The Git HTTPS transport failed during this session. Source branches and annotated tags were published through authenticated GitHub Git Data APIs with exact blob/tree equivalence, expected parents/heads and create-only tag refs. No force push, tag replacement or secret publication occurred. Original workspaces were preserved; modifications used isolated owned branches and PRs.

To repeat artifact verification, dispatch `.github/workflows/independent-release-verification.yml` in gouno-doc with repository `gosso`, `gosso-admin` or `gouno-blog`, and the exact tag source from the table. It is read-only: no signing, publication or production credentials. Local independent verification may also use the recorded exact identities/digests with `cosign verify`; never verify a floating main tag as a formal release.
