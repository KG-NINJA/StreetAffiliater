from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import subprocess

app = FastAPI()

# ✅ CORS設定を追加
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 必要に応じてGitHub PagesのURLに限定可能
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "StreetAffiliater Codex Web is running"}

@app.post("/api/comment")
async def comment_to_app(request: Request):
    data = await request.json()
    comment = data.get("comment", "")

    prompt = f"""
コメント: {comment}

上記のコメントをもとに、軽いユーモアを交えた1ページHTML/JSアプリを生成してください。
要件:
- 背景は落ち着いたブルー系
- クライアントサイドのみ
- フッターに #KGNINJA StreetAffiliater を表示
- アフィリエイトリンクを1つ自然に配置（例: Amazon）
"""

    # Codex CLI 実行（出力をHTMLとして返す）
    result = subprocess.run(
        ["codex", "run", "--model", "gpt-4o-mini", "--prompt", prompt],
        capture_output=True, text=True
    )

    return {"html": result.stdout.strip()}
