#!/usr/bin/env bash
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1

repository_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repository_root"

python -m unittest discover -s tests

while IFS= read -r example_dir; do
  python -m unittest discover -s "$example_dir" -v
done < <(find medium/examples/agentic-ai-engineering -mindepth 1 -maxdepth 1 -type d -name 'part-*' | sort)

python scripts/validate_course_lesson.py \
  --root medium/generated/agentic-ai-engineering \
  --discover-current \
  --require-schema 3

manifests=()
while IFS= read -r manifest; do
  manifests+=("$manifest")
done < <(find medium/generated/agentic-ai-engineering -name '*.json' -type f | sort)
if [ "${#manifests[@]}" -gt 0 ]; then
  python scripts/validate_article_package.py "${manifests[@]}"
fi
