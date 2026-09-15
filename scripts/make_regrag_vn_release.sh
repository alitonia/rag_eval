#!/usr/bin/env bash
# make_regrag_vn_release.sh -- rebuild the single-commit artifact repository
# github.com/alitonia/regrag-vn from the current HEAD of this repository.
#
# The release repo is a squash: exactly one root commit holding only the
# public artifact set. Development-only material (reports/, pod_artifacts/,
# docs/, Draft.docx) never enters it, so re-running replaces the single
# commit in place via force-push and re-points the release tag.
#
# Usage (from the repository root):
#   bash scripts/make_regrag_vn_release.sh
# Override the remote, tag, or release repo with environment variables:
#   REMOTE=regrag-vn TAG=v1.0.0 RELEASE_REPO=alitonia/regrag-vn
set -euo pipefail

REMOTE="${REMOTE:-regrag-vn}"
TAG="${TAG:-v1.0.0}"
RELEASE_REPO="${RELEASE_REPO:-alitonia/regrag-vn}"
MSG="feat: initial release of RegRAG-VN benchmark and artifacts"
EXCLUDE="reports pod_artifacts docs Draft.docx"

SRC="$(git rev-parse --show-toplevel)"
cd "$SRC"
REMOTE_URL="$(git remote get-url "$REMOTE")"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

git archive HEAD | tar -x -C "$WORK"
for item in $EXCLUDE; do
  rm -rf "$WORK/$item"
done

git -C "$WORK" init -q -b main
git -C "$WORK" add -A
git -C "$WORK" \
  -c user.name="$(git config user.name)" \
  -c user.email="$(git config user.email)" \
  commit -q -m "$MSG"
git -C "$WORK" tag -f "$TAG"

git -C "$WORK" push -f "$REMOTE_URL" main
git -C "$WORK" push -f "$REMOTE_URL" "$TAG"

gh release upload "$TAG" --repo "$RELEASE_REPO" --clobber "$WORK/paper/main.pdf"

echo "release repo rebuilt from source commit $(git rev-parse --short HEAD)"
git -C "$WORK" log --oneline
echo "files in release tree: $(find "$WORK" -type f -not -path "$WORK/.git/*" | wc -l)"
