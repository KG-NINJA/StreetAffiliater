#!/usr/bin/env bash
# 日本語コメント: GitHub Issueから自動PRを生成するスクリプト
set -euo pipefail

ISSUE_NUMBER="${1:-}"
if [[ -z "${ISSUE_NUMBER}" ]]; then
  echo "利用方法: $0 <issue-number>" >&2
  exit 1
fi

# 日本語コメント: 認証トークンをチェック
if [[ -z "${GH_TOKEN:-}" ]]; then
  echo "GH_TOKEN が設定されていません。" >&2
  exit 1
fi

REPO="${GITHUB_REPOSITORY:-}"
if [[ -z "${REPO}" ]]; then
  echo "GITHUB_REPOSITORY が未設定です。" >&2
  exit 1
fi

BASE_BRANCH="${BASE_BRANCH:-work}"
BRANCH_NAME="auto/issue-${ISSUE_NUMBER}-$(date +%Y%m%d%H%M%S)"
PR_TITLE="Auto update from issue #${ISSUE_NUMBER}"
PR_BODY="${PR_BODY:-Automated update generated from issue #${ISSUE_NUMBER}.}"

# 日本語コメント: 後続のPythonから参照できるように環境変数をエクスポート
export BRANCH_NAME
export BASE_BRANCH
export PR_TITLE
export PR_BODY

# 日本語コメント: Git利用者情報を初期化
GIT_USER_NAME="${GIT_USER_NAME:-codex-bot}"
GIT_USER_EMAIL="${GIT_USER_EMAIL:-bot@example.com}"
git config user.name "${GIT_USER_NAME}"
git config user.email "${GIT_USER_EMAIL}"

# 日本語コメント: ベースブランチを取得
if git rev-parse --verify "${BASE_BRANCH}" >/dev/null 2>&1; then
  git checkout "${BASE_BRANCH}"
else
  git fetch origin "${BASE_BRANCH}:${BASE_BRANCH}"
  git checkout "${BASE_BRANCH}"
fi

git pull --ff-only origin "${BASE_BRANCH}"

# 日本語コメント: 作業ブランチを作成
if git rev-parse --verify "${BRANCH_NAME}" >/dev/null 2>&1; then
  git switch "${BRANCH_NAME}"
else
  git switch -c "${BRANCH_NAME}"
fi

# 日本語コメント: ここで生成スクリプト等を呼び出す想定（存在すれば）
if [[ -x "./scripts/generate_app.sh" ]]; then
  ./scripts/generate_app.sh "${ISSUE_NUMBER}"
fi

# 日本語コメント: 変更が無ければ処理を終了
if git diff --quiet; then
  echo "変更が無いためPRは作成しません。"
  exit 0
fi

git add -A
git commit -m "${PR_TITLE}"
git push origin "${BRANCH_NAME}"

# 日本語コメント: GitHub APIを用いてPRを作成
API_ENDPOINT="https://api.github.com/repos/${REPO}/pulls"
JSON_PAYLOAD=$(python - <<'PY'
import json
import os
print(json.dumps({
    "title": os.environ["PR_TITLE"],
    "head": os.environ["BRANCH_NAME"],
    "base": os.environ["BASE_BRANCH"],
    "body": os.environ["PR_BODY"],
}))
PY
)

curl --fail --show-error --silent \
  -X POST "${API_ENDPOINT}" \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer ${GH_TOKEN}" \
  -d "${JSON_PAYLOAD}"

echo "PRを作成しました。"
