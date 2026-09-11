# Code Generation

[中文](./zh-CN/code-generation.md)

Code generation in modern Gouno is a **project-template capability**.

Gouno Core provides the Codegen protocol and execution engine. The current project/template decides whether Codegen exists and, when it does, the command name, generator catalog, arguments, flags, output paths, composition, and source templates.

There is no built-in DDD generator catalog in Gouno Core.

## Discover the current project's capabilities

The official `gouno-template` ships `.gouno/codegen.yaml` and currently exposes `gen`:

```bash
gouno gen --help
```

Another template can expose a different generator catalog, and a template with no `.gouno/codegen.yaml` can have no Codegen command at all.

Do not assume that `domain`, `repository`, `service`, `controller`, `task`, or `suite` exists until the current project's manifest/help declares it.

## Default `gouno-template` example

The official default template currently defines these generators:

```bash
gouno gen domain order
gouno gen repository order
gouno gen service order
gouno gen controller order
gouno gen task send_email
gouno gen suite order
```

The default `suite` is a template-defined composition of:

```text
domain
repository
service
```

That composition is not a Core rule.

### Default output paths

For the official default template:

| Generator | Default output |
|-----------|----------------|
| `domain` | `internal/domain/<name>.go` |
| `repository` | `internal/repository/<name>.go` |
| `service` | `internal/service/<name>.go` |
| `controller` | `internal/controller/<name>.go` |
| `task` | `internal/task/<name>.go` |

These paths come from the default template's `.gouno/codegen.yaml`.

### Default flags

The default template's individual file generators declare:

```text
--path, -p
--force, -f
```

For example:

```bash
gouno gen service order --path internal/application
gouno gen service order --force
```

The default `suite` currently declares `--force`, but does not declare a shared `--path` flag. Always use `gouno gen <generator> --help` rather than assuming every generator has the same options.

When a manifest declares a boolean flag named `force`, the Codegen v1 engine treats it as the overwrite policy. Existing files are otherwise skipped.

## Generator policy belongs to the project

A different template can define a completely different vocabulary:

```text
gouno gen handler user
gouno gen usecase user
gouno gen gateway user
```

or a single higher-level command:

```text
gouno gen module user
```

It can also omit Codegen entirely.

This is intentional: project architecture belongs to the template/project, while Gouno owns only the mechanism.

## Codegen runtime resources

A Codegen-enabled project commonly contains:

```text
.gouno/
├── codegen.yaml
└── codegen/
    └── *.tmpl
```

These files travel with the generated project. This pins generator behavior to the project's template version rather than fetching the latest remote template each time code is generated.

## Template expressions

Codegen v1 supports manifest/template functions including:

```text
arg
flag
camel
snake
kebab
lower
upper
```

For example, a source template can use a positional argument to construct a Go type name while the manifest controls the output path.

The exact expression semantics, manifest fields, composition rules, safety rules, and reserved `force` behavior are normative in the [Gouno Template Codegen Specification v1](https://github.com/rushairer/gouno/blob/main/docs/codegen-template-spec.md).

## Safety model

Codegen v1 validates project-relative template/output paths, rejects paths that escape the project, formats generated Go files, and does not provide arbitrary shell hooks or executable plugins.

Do not treat source templates as a way to bypass the project's normal review, security, package-boundary, or testing requirements. Generated code becomes normal project code once written.

## What's next

- [Project Templates](./project-templates.md) — choose and pin project templates
- [Configuration](./configuration.md) — configuration behavior of the default template
