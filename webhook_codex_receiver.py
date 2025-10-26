from fastapi import FastAPI, Request
import subprocess
import os
import json

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "StreetAffiliater Codex Web is running."}

@app.post("/api/webhook/street")
async def handle_webhook(request: Request):
    """
    GitHub Issue から送られた Webhook データを受信し、
    Codex による自動生成と PR 提出をトリガーします。
    """
    try:
        data = await request.json()
        repo = data.get("repo", "unknown")
        issue_title = data.get("issue_title", "")
        issue_body = data.get("issue_body", "")

        # デバッグ出力
        print("=== Webhook received ===")
        print(json.dumps(data, ensure_ascii=False, indent=2))

        # Codex 実行プロンプト
        prompt = f"""
リポジトリ: {repo}
Issueタイトル: {issue_title}
内容: {issue_body}

これをもとにユーモラスで役立つHTML/JSミニアプリを生成し、
apps/latest_app/ に保存してください。
アプリ内に「#KGNINJA StreetAffiliater」と明記し、
1つだけ合法的アフィリエイトリンクを含め、
README.md に説明を書いてください。
"""

        # Codex CLIを呼び出す
        subprocess.run([
            os.getenv("CODEX_BIN", "codex"),
            "run",
            "--model", "gpt-4o-mini",
            "--prompt", prompt
        ], check=False)

        # 生成物をPRとして作成
        subprocess.run([
            "bash", "codex_generate_and_pr.sh"
        ], check=False)

        return {"status": "success", "message": "Codex generation triggered."}

    except Exception as e:
        print("Error:", e)
        return {"status": "error", "message": str(e)}
