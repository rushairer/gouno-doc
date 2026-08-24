# Engineering Standard

[中文](../zh-CN/standards/engineering.md)

All Gouno repositories use Conventional Commit pull-request titles and Keep a Changelog. User-visible behavior, public configuration, generated output, and compatibility changes must be recorded under `Unreleased` before release.

GitHub Actions use complete commit SHAs, least-privilege permissions, and concurrency cancellation. Repositories enable weekly Dependabot updates for their supported package ecosystems. Production references use immutable release versions and image digests; branches and floating tags are not release inputs.

The first enforced adopters are `gouno-template`, `gouno-agent-demo`, and `gouno-cli`. Each calls the versioned reusable workflows in this repository by the full commit SHA of a released Gouno Docs version.
