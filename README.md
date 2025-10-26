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

---

## 🌟 最新アプリ: Codex Webコメントポータル
- ファイル: `apps/latest_app/index.html`
- テーマカラー: calm-blue（柔らかなブルーグラデーション）
- 概要: コメントフォームからCodex Webにリクエストを送り、応答としてニックネームと雰囲気に合わせたミニアプリ案を自動生成します。
- 使い方: コメントと雰囲気を選んで送信すると、Codex Webが名称・特徴リスト・アフィリエイト提案をまとめて表示します。
- 収益リンク: 生成プレビュー内に1つのAmazonリンクを表示し、収益が発生する可能性を明記しています。

ユーザーのインスピレーションを即座に形にするプレビューが得られるため、企画会議前の素早いアイデア出しにも重宝します。

---

## 🛠️ 使い方（エンドツーエンド）

1. **Codex Webエンドポイントを準備**
   - `https://your-codex-web.app/api/webhook/street` を、あなたのCodex WebデプロイURLに差し替えてください。
   - エンドポイントでは本リポジトリの `/api/webhook/street` のロジックが実行され、Issueイベントを解析します。
2. **Issue経由で自動生成をトリガー**
   - GitHubで新しいIssueを作成し、`auto-pr` ラベルを付与すると、`issue_trigger.yml` ワークフローが発火します。
   - ワークフローはIssueペイロードをCodex WebへPOSTし、必要に応じてCodex生成をスタートさせます。
3. **生成結果を確認**
   - Codex Webが `/apps/latest_app/index.html` などの成果物を生成し、収益リンクや `#KGNINJA StreetAffiliater` 表記を付加します。
   - 生成物はPRに含まれる前にローカルで確認できます。
4. **PR作成スクリプトを実行**
   - 生成内容をコミットしたら `./codex_generate_and_pr.sh "あなたのブランチ名" "PRタイトル"` を実行します。
   - スクリプトは最新コミットをプッシュし、GitHub API経由でPRを自動作成します。
5. **レビューとデプロイ**
   - PRが承認されると、GitHub Pagesへの公開フローが走り、最新アプリがデプロイされます。

上記ステップで、Issue作成からPR提出、デプロイまでをノーコードで回せます。利用時はGitHubトークン権限やCodex Web側のAPI制限を事前にご確認ください。
