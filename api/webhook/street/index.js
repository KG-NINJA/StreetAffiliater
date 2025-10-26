// 日本語コメント: GitHub IssuesなどのWebhookを処理するエンドポイント

/**
 * 日本語コメント: レスポンス送信のユーティリティ
 * @param {object} res - レスポンスオブジェクト
 * @param {number} status - ステータスコード
 * @param {object} payload - 返却するJSON
 */
function sendJson(res, status, payload) {
  // 日本語コメント: Next.js/Vercel互換の送信処理
  if (typeof res.status === 'function') {
    res.status(status);
  } else {
    res.statusCode = status;
  }
  if (typeof res.setHeader === 'function') {
    res.setHeader('Content-Type', 'application/json');
  }
  const body = JSON.stringify(payload);
  if (typeof res.json === 'function') {
    return res.json(payload);
  }
  if (typeof res.send === 'function') {
    return res.send(body);
  }
  return res.end ? res.end(body) : body;
}

/**
 * 日本語コメント: リクエストボディを安全に取り出す
 * @param {object} req - リクエストオブジェクト
 * @returns {any}
 */
function readBody(req) {
  if (req.body && Object.keys(req.body).length > 0) {
    return req.body;
  }
  if (req.rawBody) {
    try {
      return JSON.parse(req.rawBody.toString());
    } catch (error) {
      return {};
    }
  }
  return {};
}

module.exports = async function handler(req, res) {
  // 日本語コメント: POST以外は拒否
  const method = req.method || req.httpMethod;
  if (method && method.toUpperCase() !== 'POST') {
    return sendJson(res, 405, { message: 'Method Not Allowed' });
  }

  const body = readBody(req);
  const { action, issue, pull_request: pr, comment } = body;

  // 日本語コメント: 解析済みサマリを作成
  const summary = {
    action: action || 'unknown',
    hasIssue: Boolean(issue),
    hasPullRequest: Boolean(pr),
    hasComment: Boolean(comment),
  };

  // 日本語コメント: 自動生成が必要かを判定
  const requiresGeneration = Boolean(
    issue &&
      Array.isArray(issue.labels) &&
      issue.labels.some((label) => (label.name || label) === 'auto-pr')
  );

  // 日本語コメント: 応答本文を組み立て
  const response = {
    ok: true,
    summary,
    nextAction: requiresGeneration ? 'run-codex-generate' : 'no-action',
    issue: issue
      ? {
          number: issue.number,
          title: issue.title,
          url: issue.html_url,
        }
      : null,
  };

  return sendJson(res, 200, response);
};
