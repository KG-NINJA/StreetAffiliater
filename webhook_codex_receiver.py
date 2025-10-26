from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import aiohttp, os, json

app = FastAPI()

# CORS許可（フロントのGitHub Pagesからアクセス可）
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

以下の要件を満たす実行可能なHTML+JavaScriptアプリを生成してください。
- 1ファイルで動作する（index.html形式）
- 完全にブラウザ側で動く
- JSコードは<body>内に埋め込む
- 外部ライブラリを使う場合はCDNを利用
- アフィリエイトリンクを自然に配置
- コード以外の説明文は不要。純粋なHTMLだけを返す
- フッターに #KGNINJA #StreetAffiliater を表示
- 内容に関連するアフィリエイトリンクを1つ自然に配置（例: Amazon）
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
        async with session.post("https://api.openai.com/v1/responses", headers=headers, json=body) as resp:
            data = await resp.json()
            try:
                html = data["output"][0]["content"][0]["text"]
            except Exception:
                html = "<pre>" + json.dumps(data, ensure_ascii=False, indent=2) + "</pre>"
            return HTMLResponse(content=html, status_code=200)
