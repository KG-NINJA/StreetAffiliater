from fastapi import FastAPI, Request
import subprocess
import json

app = FastAPI()

@app.get("/")
def root():
    return {"status": "StreetAffiliater Codex Web is running"}

@app.post("/api/webhook/street")
async def handle_webhook(request: Request):
    data = await request.json()
    issue_title = data.get("title")
    issue_body = data.get("body")
    repo = data.get("repo")

    print(f"Received issue from {repo}: {issue_title}")

    # Codex CLI 実行（PR生成シミュレーション）
    result = subprocess.run([
        "echo", f"Generating app for: {issue_title}"
    ], capture_output=True, text=True)

    print(result.stdout)
    return {"status": "ok", "message": result.stdout}
@app.post("/api/comment")
async def comment_to_app(request: Request):
    data = await request.json()
    comment = data.get("comment", "")

    # Codexへ指示するプロンプト
    prompt = f"""
コメント: {comment}

上記のコメントをもとに、軽いユーモアを交えた1ページHTML/JSアプリを生成してください。
要件:
- 背景は落ち着いたブルー系
- クライアントサイドのみ
- フッターに #KGNINJA StreetAffiliater を表示
- アフィリエイトリンクを1つ自然に配置（例: Amazon）
"""

    result = subprocess.run(
        ["codex", "run", "--model", "gpt-4o-mini", "--prompt", prompt],
        capture_output=True, text=True
    )

    return {"html": result.stdout.strip()}
