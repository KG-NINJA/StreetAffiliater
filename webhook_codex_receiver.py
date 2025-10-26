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
    return {
        "status": "StreetAffiliater v3 is running (Codex Cloud mode)",
        "model": os.getenv("CODEX_MODEL", "gpt-4o")
    }

@app.post("/api/comment")
async def comment_to_app(request: Request):
    data = await request.json()
    comment = data.get("comment", "")

    # Codexへプロンプト
    prompt = f"""
ユーザーから次のコメントが届きました:
「{comment}」

あなたの役割は「AIアプリ生成エンジン」です。
以下の条件を満たす **実行可能なHTML+JavaScriptアプリ** を生成してください。

🎯 要件:
- 1ファイル完結（index.html形式）
- 完全にブラウザ上で動作
- コメント内容からアプリのテーマを推定して作成（例: 音楽→音再生, ゲーム→クリック反応, 犬→鳴き声, 天気→API表示など）
- 背景はMatrix風（canvasアニメーション）ローディング付き
- フッターに「#KGNINJA #StreetAffiliater」
- 外部ライブラリはCDN利用のみ
- 必ず関連する **Amazonアフィリエイトリンク** を1つ自然に含める（URL例: https://www.amazon.co.jp/dp/<ASIN>）
- コメント内容に最も関連する商品を自動選択（例: 犬→ドッグフード、音楽→スピーカー、カメラ→三脚）
- コード以外の説明文やマークダウン記号は不要
- 純粋なHTMLコードのみを出力

例:
コメント「柴犬が遊べるアプリ」
→ 犬の音＋クリックイベント＋犬用品のAmazonリンク入りHTMLを生成
"""

    headers = {
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
        "Content-Type": "application/json",
    }

    body = {
        "model": os.getenv("CODEX_MODEL", "gpt-4o"),
        "input": prompt
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://api.openai.com/v1/responses", headers=headers, json=body
        ) as resp:
            data = await resp.json()
            try:
                html = data["output"][0]["content"][0]["text"]
                if "```" in html:
                    html = html.split("```")[-2]
            except Exception:
                html = json.dumps(data, ensure_ascii=False)
            return {"html": html}
