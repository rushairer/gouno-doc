# Authoring a Gouno Project Template

[中文](./zh-CN/template-authoring.md)

A Gouno Project Template is a full Go project skeleton consumed by `gouno-cli new`.

The most important design rule is simple:

> **Gouno owns mechanisms; your template owns project policy.**

Your template can choose its own framework, directory structure, dependency set, architecture, configuration approach, engineering rules, and optional Codegen catalog. The official [`gouno-template`](https://github.com/rushairer/gouno-template) is a reference implementation, not a base class that every template must copy.

This guide explains an authoring workflow. The normative bootstrap behavior lives in the [`gouno-cli` Project Template Contract v1](https://github.com/rushairer/gouno-cli/blob/main/docs/project-template-contract.md), and the optional Codegen protocol lives in the [`gouno` Codegen Specification v1](https://github.com/rushairer/gouno/blob/main/docs/codegen-template-spec.md).

## 1. Start with the smallest possible template

Do not start by copying the default template unless you actually want its architecture.

A minimal template can look like this:

```text
my-gouno-template/
├── cmd/
│   └── main.go
├── go.mod
└── README.md
```

`go.mod`:

```go
module {{.ModulePath}}

go 1.25.0
```

`cmd/main.go`:

```go
package main

import "fmt"

func main() {
    fmt.Println("{{.ProjectName}}")
}
```

That is already enough to demonstrate the Project Template Contract. It does not need Gin, Cobra, DDD, Gouno runtime packages, or Codegen.

### Test it locally

From a directory outside the template repository:

```bash
gouno-cli new demo-service \
  -t /absolute/path/to/my-gouno-template \
  -m example.com/demo-service
```

Then inspect and test the generated project:

```bash
cd demo-service
go mod tidy
go build ./...
go test ./...
```

The generated `go.mod` should use `example.com/demo-service`, and the generated program should contain `demo-service` where the project-name variable was used.

## 2. Understand Stage 1: project bootstrap

`gouno-cli new` is the first rendering stage.

Its bootstrap data is intentionally small:

```text
{{.ModulePath}}
{{.ProjectName}}
```

Use these values only where the initial project must differ from the template source, for example:

- `module` in `go.mod`;
- imports that contain the new module path;
- package/project labels;
- default local filenames or identifiers derived from the project name.

The exact parse/copy/rollback rules are part of the Project Template Contract. Do not build a template around undocumented behavior.

### Important reserved paths

`gouno-cli` currently filters several private/reserved path segments. In particular, the top-level/path-segment name:

```text
templates/
```

is a **legacy reserved path** retained for compatibility with older Gouno versions. It is not the Codegen v1 directory.

Do not place modern generator resources there. Use `.gouno/codegen/` for Codegen v1.

## 3. Decide whether your generated project needs Gouno runtime packages

A Project Template does not conceptually have to depend on the `github.com/rushairer/gouno` module.

Use Gouno runtime packages when your generated project intentionally wants reusable Gouno mechanisms, for example the Codegen runtime or selected middleware/response helpers. Keep your application architecture in the project/template.

Avoid importing Gouno merely to encode a directory convention or a business-layer abstraction. Those are template concerns.

If the template declares a Gouno dependency, pin a released version in release-ready template sources. Do not publish a template that relies on a local `replace` directive or an unreleased pseudo-version unless that is explicitly the intended development-only state.

## 4. Codegen is optional

A template without `.gouno/codegen.yaml` can have no Codegen command at all. This is a valid and supported design.

If your team benefits from repeatable source generation, opt into Codegen v1 explicitly.

A small Codegen-enabled template might add:

```text
my-gouno-template/
├── .gouno/
│   ├── codegen.yaml
│   └── codegen/
│       └── handler.tmpl
├── cmd/
│   └── ...
├── go.mod
└── ...
```

For example, your architecture may use `handler` instead of the default template's `controller/service/...` vocabulary.

`.gouno/codegen.yaml`:

```yaml
schema: gouno.dev/codegen/v1
command:
  use: gen
  short: Generate project code

generators:
  - name: handler
    short: Generate an HTTP handler
    args:
      - name: name
        required: true
    flags:
      - name: path
        shorthand: p
        type: string
        default: internal/handler
        description: output directory
      - name: force
        shorthand: f
        type: bool
        default: false
        description: overwrite an existing file
    outputs:
      - template: .gouno/codegen/handler.tmpl
        path: '{{ flag "path" }}/{{ arg "name" }}.go'
```

A corresponding `handler.tmpl` could contain:

```go
package handler

type {{ camel (arg "name") }}Handler struct{}
```

The resulting project can expose:

```bash
gouno gen handler user
```

The names `gen` and `handler` are template policy. Another template can choose a different Codegen command name or generator catalog.

Do not copy the full Codegen schema into your own documentation as a second specification. Link to the normative [Codegen Specification v1](https://github.com/rushairer/gouno/blob/main/docs/codegen-template-spec.md) for supported fields, expressions, composition, overwrite behavior, and safety rules.

## 5. Attach the project-aware Codegen command

A manifest alone is data. A project CLI that wants Gouno Codegen also needs to attach the project command through the Gouno runtime.

The official template currently uses the equivalent of:

```go
package projectcli

import (
    "log"

    "github.com/rushairer/gouno/generator"
    "github.com/spf13/cobra"
)

var rootCmd = &cobra.Command{Use: "my-project"}

func Execute() {
    if _, err := generator.AttachProjectCommand(rootCmd, ""); err != nil {
        log.Fatalf("load project commands: %v", err)
    }
    if err := rootCmd.Execute(); err != nil {
        log.Fatal(err)
    }
}
```

`AttachProjectCommand` discovers the current project's manifest and attaches the manifest-defined command when present. If the manifest is absent, no Codegen command is attached.

How you structure the rest of your Cobra CLI is your template's decision.

## 6. Understand Stage 2: project Codegen

A Codegen-enabled template contains two different template languages with two different lifetimes:

```text
┌─────────────────────────────────────────────┐
│ Stage 1 — Project Bootstrap                 │
│ owner: gouno-cli                            │
│ command: gouno-cli new                      │
│ values: ModulePath / ProjectName            │
└───────────────────┬─────────────────────────┘
                    │ generated project
                    ▼
┌─────────────────────────────────────────────┐
│ Stage 2 — Project Codegen (optional)        │
│ owner: Gouno protocol + project policy      │
│ command: manifest-defined, often gouno gen  │
│ values: args / flags / Codegen functions    │
└─────────────────────────────────────────────┘
```

The boundary is explicit:

```text
.gouno/codegen.yaml
.gouno/codegen/**
```

Those files are copied verbatim during Stage 1 so Codegen expressions survive until Stage 2.

Do not depend on ordinary Stage-1 parse failures to protect Stage-2 syntax. Put Codegen runtime data under the defined `.gouno/codegen*` boundary.

## 7. Keep architecture and generators synchronized

Once a template owns generator policy, its manifest becomes part of the template's development contract.

If you change:

```text
internal/service/
```

to:

```text
internal/application/
```

then update the corresponding generator output paths and source templates in the same change.

A useful rule is:

> If generated code repeatedly needs manual repair, fix the template/generator rather than teaching every project to repair the same output.

Generated code is ordinary project code after it is written. It should obey the same package boundaries, security controls, lint rules, error conventions, and tests as handwritten code.

## 8. Decide intentionally what files the generated project should inherit

Today, `gouno-cli` does not provide a general `.gounoignore` or source-only manifest for template repositories.

Except for the documented filtered/reserved paths, treat files in the template repository as potential generated-project files.

This matters for files such as:

```text
AGENTS.md
.github/
scripts/
docs/
Makefile
```

Ask a simple question before adding one:

> Should a project created from this template also receive this file?

If yes, design it as part of the project contract. If no, do not invent an undocumented hidden-directory convention and assume the CLI will exclude it.

### Shipping `AGENTS.md`

An `AGENTS.md` can be especially valuable in an AI-assisted engineering template because it transfers development invariants together with the source layout.

Good inherited rules include:

- package/layer boundaries that belong to this template;
- where Codegen policy lives;
- required tests and security checks;
- rules for generated code;
- project-specific dependency or configuration boundaries.

Do **not** put template-repository-maintainer-only instructions in a root `AGENTS.md` if they make no sense in generated projects. Until a general source-only mechanism exists, root `AGENTS.md` should remain valid downstream.

See the official [`gouno-template/AGENTS.md`](https://github.com/rushairer/gouno-template/blob/main/AGENTS.md) as a reference for this pattern.

## 9. Build a repeatable template verification script

Do not test only the template repository itself. Test the **rendered project**.

A good verification flow is:

```text
render/create a temporary project
        ↓
verify module files are stable
        ↓
go mod tidy / download
        ↓
build + test
        ↓
if Codegen exists:
  inspect help
  run representative generators
  run composition generators
  compile/test generated output
        ↓
gofmt / vet / lint / vulnerability checks
```

The official [`gouno-template/scripts/verify-template.sh`](https://github.com/rushairer/gouno-template/blob/main/scripts/verify-template.sh) is a reference implementation of this style. Your template's script should reflect **your** architecture and generator catalog rather than copying its exact DDD smoke tests blindly.

At minimum, for a Go template:

```bash
go mod tidy
go test ./...
go vet ./...
```

Production-oriented templates should usually add race testing, linting, vulnerability scanning, and any architecture/security checks their generated projects require.

### Reusable CI

`gouno-doc` provides a reusable project-template quality workflow that runs the template's `scripts/verify-template.sh` across the supported Go matrix.

A consumer can call it from its own workflow using a **full commit SHA from a released gouno-doc version**:

```yaml
jobs:
  template-quality:
    uses: rushairer/gouno-doc/.github/workflows/project-template-quality.yml@<released-gouno-doc-commit-sha>
```

Do not pin production CI to `@main` or another moving ref.

## 10. Test through the real CLI before release

Before tagging your template, test the same path users will use.

For a local candidate:

```bash
gouno-cli new template-smoke \
  -t /absolute/path/to/your-template \
  -m example.com/template-smoke
```

For a pushed release candidate, test its remote ref:

```bash
gouno-cli new template-smoke \
  -t https://github.com/yourorg/your-template \
  --template-ref your-release-candidate-ref \
  -m example.com/template-smoke
```

Then verify the generated project, not just the source template repository.

If Codegen is enabled, also verify:

```bash
./your-project-command --help
./your-project-command gen --help
./your-project-command gen <representative-generator> smoke
```

Use the actual command name declared by your project; `gen` is only a common/default choice.

## 11. Publish immutable template versions

Once a template version is verified, publish an immutable Git tag and tell users to pin it with `--template-ref` when reproducibility matters.

Example:

```bash
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

Consumer:

```bash
gouno-cli new billing-service \
  -t https://github.com/yourorg/your-template \
  --template-ref v1.0.0 \
  -m github.com/yourorg/billing-service
```

Treat template versions as real engineering releases: document architecture changes, dependency changes, generated-output changes, Codegen changes, and compatibility requirements.

## 12. Suggested template repository shape

This is a suggestion, not a required architecture:

```text
my-gouno-template/
├── .github/                 # CI that generated projects should also inherit, if intentional
├── .gouno/                  # only when project tooling such as Codegen is enabled
│   ├── codegen.yaml
│   └── codegen/
├── cmd/
├── internal/                # your architecture, not Gouno's
├── scripts/                 # scripts useful in generated projects, if intentional
├── AGENTS.md                # optional inherited project engineering contract
├── CHANGELOG.md
├── Makefile
├── README.md
├── go.mod
└── go.sum
```

You can make it much smaller. The contract does not require these directories.

## 13. What not to do

Avoid these failure modes:

- copying the official template and assuming its architecture is mandatory;
- putting modern Codegen resources under the legacy `templates/` path;
- adding a generator name to documentation without declaring it in the manifest;
- fetching the latest remote generator templates every time `gouno gen` runs;
- letting Stage 1 consume Stage 2 Codegen expressions;
- publishing pseudo-versions or local `replace` directives unintentionally;
- placing maintainer-only instructions in files that will be inherited by generated projects;
- weakening generated-project tests merely to make the template CI green.

## 14. About a future `template validate` tool

There is currently no public `gouno-cli template validate` command.

A lightweight validator may be useful in the future, but it should implement the already-stable Project Template Contract rather than invent new semantics. A good future validator could report which files will be rendered, copied verbatim, or filtered; validate Codegen resources; create a temporary project; and run configured verification hooks without turning Gouno into a template package manager.

For now, the authoritative path is:

```text
Project Template Contract
        ↓
this authoring guide
        ↓
your template + verification script
        ↓
gouno-cli new smoke test
        ↓
immutable release
```

## References

- [Project Templates: using and pinning templates](./project-templates.md)
- [Code Generation: using template-defined generators](./code-generation.md)
- [Gouno Project Template Contract v1](https://github.com/rushairer/gouno-cli/blob/main/docs/project-template-contract.md)
- [Gouno Template Codegen Specification v1](https://github.com/rushairer/gouno/blob/main/docs/codegen-template-spec.md)
- [Official default template](https://github.com/rushairer/gouno-template)
