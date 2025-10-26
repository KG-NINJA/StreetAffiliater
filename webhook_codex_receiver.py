from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
import aiohttp, os, json, asyncio

APP_TITLE = "StreetAffiliater Codex Web"
OPENAI_URL = "https://api.openai.com/v1/responses"
MODEL_DEFAULT = "gpt-4o-mini"
TIMEOUT_SECS = 60

app = FastAPI(title=APP_TITLE)

# CORS（必要なら allow_origins を GitHub Pages のURLに限定可）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "status": f"{APP_TITLE} is running (OpenAI Codex Cloud mode)",
        "model": os.getenv("CODEX_MODEL", MODEL_DEFAULT),
    }

def build_prompt(comment: str) -> str:
    return f"""
コメント: {comment}

以下の要件を満たす実行可能なHTML+JavaScriptアプリを生成してください。
- 1ファイルで動作する（index.html形式）
- 完全にブラウザ側で動作する
- JSコードは<body>内に埋め込む
- 外部ライブラリを使う場合はCDNを利用
- 背景は落ち着いたブルー系（calm blue）
- フッターに #KGNINJA #StreetAffiliater を表示
- 内容に関連するアフィリエイトリンクを1つ自然に配置（例: Amazon）
- コード以外の説明文は不要。純粋なHTMLだけを返す
"""

def clean_fences(text: str) -> str:
    # ```html や ``` を除去
    return text.replace("```html", "").replace("```", "").strip()

@app.post("/api/comment")
async def comment_to_app(request: Request):
    try:
        data = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON"}, status_code=400)

    comment = (data.get("comment") or "").strip()
    if not comment:
        return JSONResponse({"error": "コメントが空です"}, status_code=400)

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return JSONResponse({"error": "OPENAI_API_KEY が未設定です"}, status_code=500)

    prompt = build_prompt(comment)
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    body = {
        "model": os.getenv("CODEX_MODEL", MODEL_DEFAULT),
        "input": prompt,
    }

    try:
        timeout = aiohttp.ClientTimeout(total=TIMEOUT_SECS)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(OPENAI_URL, headers=headers, json=body) as resp:
                # OpenAI 側エラー可視化
                if resp.status >= 400:
                    txt = await resp.text()
                    return JSONResponse({"error": "OpenAI error", "detail": txt}, status_code=resp.status)

                payload = await resp.json()
                # 標準的な Responses API 取り出し
                html = None
                try:
                    html = payload["output"][0]["content[0]"]["text"]  # 万一のキータイプに備えて下でフォールバック
                except Exception:
                    try:
                        html = payload["output"][0]["content"][0]["text"]
                    except Exception:
                        # 予期外構造 → そのまま可視化
                        pretty = json.dumps(payload, ensure_ascii=False, indent=2)
                        return HTMLResponse(content=f"<pre>{pretty}</pre>", status_code=200)

                html = clean_fences(html)
                # 念のため最低限のHTMLタグがあるかチェックし、なければ包む
                if "<html" not in html.lower():
                    html = f"<!DOCTYPE html><html><head><meta charset='UTF-8'><title>Auto App</title></head><body>{html}</body></html>"

                return HTMLResponse(content=html, status_code=200)

    except asyncio.TimeoutError:
        return JSONResponse({"error": "OpenAI API timeout"}, status_code=504)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
