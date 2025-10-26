from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
import aiohttp, os, json

# FastAPIアプリ初期化
app = FastAPI(title="StreetAffiliater Codex Web")

# 🔓 CORSを許可（フロントからアクセス可能に）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🌐 動作確認用エンドポイント
@app.get("/")
def root():
    return {
        "status": "StreetAffiliater Codex Web is running (OpenAI Codex Cloud mode)",
        "mode": "Cloud",
        "author": "KGNINJA",
    }

# 💬 コメントからWebアプリ生成
@app.post("/api/comment")
async def comment_to_app(request: Request):
    try:
        data = await request.json()
        comment = data.get("comment", "").strip()

        if not comment:
            return JSONResponse({"error": "コメントが空です"}, status_code=400)

        # Codex Cloud向けプロンプト
        prompt = f"""
コメント: {comment}

以下の要件を満たす実行可能なHTML+JavaScriptアプリを生成してください。
- 1ファイルで動作する（index.html形式）
- 完全にブラウザ側で動作する
- JSコードは<body>内に埋め込む
- 外部ライブラリを使う場合はCDNを利用
- コード以外の説明文は不要。純粋なHTMLのみを返す
- 背景は落ち着いたブルー系
- フッターに #KGNINJA #StreetAffiliater を表示
- 内容に関連するアフィリエイトリンクを1つ自然に配置（例: Amazon）
"""

        headers = {
            "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
            "Content-Type": "application/json",
        }

        body = {
            "model": os.getenv("CODEX_MODEL", "gpt-4o-mini"),
            "input": prompt,
        }

        # Codex Cloud API呼び出し
        async with aiohttp.ClientSession() as session:
            async with session.post("https://api.openai.com/v1/responses", headers=headers, json=body) as resp:
                data = await resp.json()

                # 出力抽出とクリーニング
                try:
                    html = data["output"][0]["content"][0]["text"]
                    html = html.replace("```html", "").replace("```", "").strip()
                except Exception:
                    html = "<pre>" + json.dumps(data, ensure_ascii=False, indent=2) + "</pre>"

                return HTMLResponse(content=html, status_code=200)

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
