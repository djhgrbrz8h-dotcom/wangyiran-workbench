export default {
  async fetch(request, env) {
    // CORS
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type',
        }
      });
    }

    const url = new URL(request.url);

    // POST /backup - 备份数据
    if (request.method === 'POST' && url.pathname === '/backup') {
      try {
        const body = await request.json();
        const data = JSON.stringify(body.data || body);
        const date = body.date || new Date().toISOString().slice(0, 10);

        // 获取当前 backup.json 的 sha
        const getResp = await fetch(
          `https://api.github.com/repos/${env.GITHUB_OWNER}/${env.GITHUB_REPO}/contents/backup.json`,
          { headers: { Authorization: `Bearer ${env.GITHUB_TOKEN}`, Accept: 'application/vnd.github.v3+json', 'User-Agent': 'wyr-backup' } }
        );
        const fileInfo = await getResp.json();

        const payload = {
          message: `Auto backup ${date}`,
          content: btoa(unescape(encodeURIComponent(data))),
          branch: 'master'
        };
        if (fileInfo.sha) payload.sha = fileInfo.sha;

        const putResp = await fetch(
          `https://api.github.com/repos/${env.GITHUB_OWNER}/${env.GITHUB_REPO}/contents/backup.json`,
          {
            method: 'PUT',
            headers: { Authorization: `Bearer ${env.GITHUB_TOKEN}`, 'Content-Type': 'application/json', Accept: 'application/vnd.github.v3+json', 'User-Agent': 'wyr-backup' },
            body: JSON.stringify(payload)
          }
        );

        if (putResp.ok) {
          return new Response(JSON.stringify({ ok: true, date }), {
            headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' }
          });
        }
        return new Response(JSON.stringify({ ok: false, error: 'GitHub API error' }), {
          status: 500, headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' }
        });
      } catch (e) {
        return new Response(JSON.stringify({ ok: false, error: e.message }), {
          status: 500, headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' }
        });
      }
    }

    return new Response('wyr-backup worker', {
      headers: { 'Content-Type': 'text/plain', 'Access-Control-Allow-Origin': '*' }
    });
  }
};
