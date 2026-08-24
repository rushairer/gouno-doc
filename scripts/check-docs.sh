#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root"

for english in standards/*.md; do test -f "zh-CN/$english"; done
for chinese in zh-CN/standards/*.md; do test -f "${chinese#zh-CN/}"; done

while IFS= read -r workflow; do
  grep -q '^permissions:' "$workflow"
  if grep -Eq '^[[:space:]]*uses: .*@(main|master|v[0-9]+(\.[0-9]+){0,2})[[:space:]]*$' "$workflow"; then
    echo "workflow action must use a full commit SHA: $workflow" >&2
    exit 1
  fi
done < <(find .github/workflows -type f -name '*.yml' -print)

while IFS= read -r document; do
  while IFS= read -r target; do
    case "$target" in http:*|https:*|mailto:*|'#'*|'') continue ;; esac
    target="${target%%#*}"
    test -e "$(dirname "$document")/$target" || { echo "broken relative link in $document: $target" >&2; exit 1; }
  done < <(perl -ne 'while (/\]\((?!<)([^ )]+)(?:\s+[^)]*)?\)/g) { print "$1\n" }' "$document")
done < <(find . -path './.git' -prune -o -name '*.md' -type f -print)
