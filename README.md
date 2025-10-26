# StreetAffiliater


**StreetAffiliater** は、Codex Webサブスクだけで回る「自動アフィリエイト生成＋PR提出システム」です。  
ユーザーコメントやトレンド情報をもとに、毎回違うユーモアのあるWebアプリを生成し、  
GitHub Pages上に公開、収益リンクを自動で挿入します。

---

### 🔁 仕組み

1. GitHub Actionsが `trigger_codex_web.yml` を起動  
2. Codex Web が `prompt.txt` の内容を使ってアプリを自動生成  
3. 生成物を `apps/latest_app/` に保存  
4. `codex_generate_and_pr.sh` によりブランチ作成＋PR作成  
5. 承認されると自動デプロイ（GitHub Pages）

---

### 💰 収益構造

- クリックや購入を促す「おすすめリンク」を挿入（合法的アフィリエイト）
- Codex Web は ChatGPT Plus サブスク内で稼働 → API課金ゼロ
- GitHub Actions と Pages は無料枠で動作

---

### ⚙️ 設定
1. `.github/workflows/trigger_codex_web.yml` にある  
   `https://your-codex-web.app/api/webhook/street` を、  
   あなたのCodex WebエンドポイントURLに置き換えてください。
2. `prompt.txt` に生成方針を記述
3. GitHub Personal Access Tokenを `GH_TOKEN` として登録（PR作成用）

---

### 📄 署名ポリシー
すべての生成物には `#KGNINJA` タグを埋め込みます。
