# gouno Documentation

[中文文档](./zh-CN/)

---

Gouno separates project bootstrap, reusable runtime/tooling mechanisms, and project-specific policy:

```text
gouno-cli       project-template bootstrap mechanics
gouno           reusable mechanisms + Codegen protocol/runtime
gouno-template  official default project/template policy
gouno-doc       user guides + engineering/compatibility standards
```

The official template is a reference implementation. Its Gin/Cobra/Viper choices, Flat Layered architecture, and concrete generator names are not requirements imposed by Gouno Core.

## Guides

- [Getting Started](./getting-started.md) — install the CLI, create a project, and run the default template
- [Project Templates](./project-templates.md) — select, pin, and use full project templates
- [Template Authoring](./template-authoring.md) — design, validate, and publish your own Gouno project template
- [Architecture Profiles](./architecture-profiles.md) — choose between the Flat Layered and Capability Module reference profiles
- [Code Generation](./code-generation.md) — use template-defined Codegen capabilities
- [Configuration](./configuration.md) — configuration behavior of the default template
- [Middleware](./middleware.md) — reusable middleware and default-template wiring
- [Engineering Standard](./standards/engineering.md) — shared repository and CI policy
- [Go Support Policy](./standards/go-support.md) — supported Go versions and quality gates
- [Release Standard](./standards/release.md) — immutable release and branch-protection gate
- [Compatibility Matrix](./standards/compatibility.md) — released repository combinations

## Normative contracts

User guides in this repository explain the contracts but do not redefine them:

- Codegen protocol/schema: [`rushairer/gouno/docs/codegen-template-spec.md`](https://github.com/rushairer/gouno/blob/main/docs/codegen-template-spec.md)
- Project bootstrap semantics: [`rushairer/gouno-cli/docs/project-template-contract.md`](https://github.com/rushairer/gouno-cli/blob/main/docs/project-template-contract.md)

Architecture Profiles are ecosystem guidance owned by `gouno-doc`; they remain project/template conventions rather than Gouno Core protocol requirements.

## Related repositories

| Repository | Description |
|------------|-------------|
| [gouno](https://github.com/rushairer/gouno) | Reusable mechanisms plus the Codegen protocol/runtime |
| [gouno-cli](https://github.com/rushairer/gouno-cli) | Architecture-agnostic project-template bootstrap CLI |
| [gouno-template](https://github.com/rushairer/gouno-template) | Official default Flat Layered template and reference Codegen policy |
