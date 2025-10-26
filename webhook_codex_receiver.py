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
    return {"status": "StreetAffiliater Codex Web is running (OpenAI Codex Cloud mode)"}

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

    headers = {
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
        "Content-Type": "application/json",
    }

    body = {
        "model": os.getenv("CODEX_MODEL", "gpt-4o-mini"),
        "input": prompt
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://api.openai.com/v1/responses", headers=headers, json=body
        ) as resp:
            data = await resp.json()
            try:
                html = data["output"][0]["content"][0]["text"]
            except Exception:
                html = json.dumps(data, ensure_ascii=False)
            return {"html": html}
