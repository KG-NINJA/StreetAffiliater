from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import aiohttp, os, json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "StreetAffiliater Codex Web is running (Cloud API mode)"}

@app.post("/api/comment")
async def comment_to_app(request: Request):
    data = await request.json()
    comment = data.get("comment", "")

    # プロンプト生成
    prompt = f"""
コメント: {comment}

上記のコメントをもとに、軽いユーモアを交えた1ページHTML/JSアプリを生成してください。
要件:
- 背景は落ち着いたブルー系
- クライアントサイドのみ
- フッターに #KGNINJA StreetAffiliater を表示
- アフィリエイトリンクを1つ自然に配置（例: Amazon）
"""

    # Codex Cloud API 情報
    endpoint = os.getenv("CODEX_ENDPOINT", "https://api.codex.cloud/v1/run")
    token = os.getenv("CODEX_TOKEN")
    model = os.getenv("CODEX_MODEL", "gpt-4o-mini")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    payload = {"model": model, "prompt": prompt, "sandbox": "workspace-write"}

    async with aiohttp.ClientSession() as session:
        async with session.post(endpoint, headers=headers, data=json.dumps(payload)) as r:
            text = await r.text()
            try:
                result = json.loads(text)
                return {"html": result.get("output", text)}
            except Exception:
                return {"html": text}
