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
