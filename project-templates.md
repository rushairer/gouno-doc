# Project Templates

[中文](./zh-CN/project-templates.md)

A Gouno **Project Template** is a full project skeleton consumed by `gouno-cli new`.

A template owns its project structure and development conventions. It may choose Gin, Echo, Fiber, net/http, DDD, Clean Architecture, another architecture, or no particular layering at all. The official [`gouno-template`](https://github.com/rushairer/gouno-template) is the default reference template, not a mandatory architecture.

## Use the default template

```bash
gouno-cli new my-service -m github.com/you/my-service
```

With the normal default setup, `gouno-cli` uses the official template when a local `./templates` directory is not present.

## Use a custom remote template

HTTPS:

```bash
gouno-cli new my-service \
  -t https://github.com/myorg/custom-gouno-template \
  -m github.com/myorg/my-service
```

SSH:

```bash
gouno-cli new my-service \
  -t git@github.com:myorg/custom-gouno-template.git \
  -m github.com/myorg/my-service
```

## Pin a template version

Remote templates follow their default branch unless `--template-ref` is provided.

For reproducible project creation, prefer an immutable release tag:

```bash
gouno-cli new my-service \
  -t https://github.com/myorg/custom-gouno-template \
  --template-ref v2.3.0 \
  -m github.com/myorg/my-service
```

A moving branch is useful during template development but is not an immutable release input.

## Use a local template

```bash
gouno-cli new my-service \
  -t /path/to/my-local-template \
  -m github.com/you/my-service
```

This is useful while developing and testing a project template before publishing it.

## Bootstrap behavior

At a high level, `gouno-cli new`:

1. clones or reads the selected full project template;
2. renders first-stage project values such as `{{.ModulePath}}` and `{{.ProjectName}}` in ordinary bootstrap files;
3. copies Codegen v1 runtime resources under `.gouno/codegen*` verbatim;
4. filters reserved/private paths;
5. preserves executable permissions subject to the bootstrap safety mask;
6. runs `go mod tidy` unless `--skip-tidy` is supplied;
7. removes a partial destination when rendering or module tidying fails.

The exact behavior is normative in the [`gouno-cli` Project Template Contract v1](https://github.com/rushairer/gouno-cli/blob/main/docs/project-template-contract.md). This guide intentionally does not duplicate that specification.

### Two template stages

A Codegen-enabled project can contain two independent rendering stages:

```text
Stage 1: gouno-cli new
  bootstrap data: ModulePath / ProjectName

Stage 2: gouno gen ...
  project Codegen data: arguments / flags / Codegen functions
```

`.gouno/codegen.yaml` and `.gouno/codegen/**` are raw-copied in Stage 1 so Stage 2 expressions survive project creation.

A project template does **not** have to provide Codegen. If it omits `.gouno/codegen.yaml`, the resulting project can have no `gen` command at all.

## Legacy `templates/` path

`gouno-cli` still filters a path segment named `templates/` for historical compatibility with older Gouno template repositories.

That directory is **not** the Codegen v1 location. New Codegen-enabled templates use:

```text
.gouno/codegen.yaml
.gouno/codegen/
```

Do not depend on `templates/` being copied into a generated project.

## About authoring templates

A custom template starts from the Project Template Contract, not from the default template's DDD/Gin structure. The simplest valid template can be only a small project skeleton with bootstrap variables and no Codegen at all.

The official [`gouno-template`](https://github.com/rushairer/gouno-template) is useful as a reference implementation for a production-oriented default stack, but copying all of its architectural choices is optional.

Until using a dedicated authoring guide, validate custom templates by generating a temporary project with `gouno-cli new`, running `go mod tidy`, and executing the generated project's build/test checks. Do not document a `template validate` subcommand as available; no such public command exists yet.

## What's next

- [Code Generation](./code-generation.md) — understand template-defined Codegen capabilities
- [Configuration](./configuration.md) — configuration used by the default template
