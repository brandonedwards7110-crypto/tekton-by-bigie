const SESSION_COOKIE = "tekton_auth";
const RESET_COOKIE = "tekton_reset";
const SESSION_TTL_SECONDS = 60 * 60 * 24 * 30; // 30 days
const RESET_TTL_SECONDS = 60 * 10; // 10 minutes to finish a password reset

function b64urlEncode(str) {
  return btoa(str).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
}
function b64urlDecode(str) {
  str = str.replace(/-/g, "+").replace(/_/g, "/");
  while (str.length % 4) str += "=";
  return atob(str);
}

async function hmac(key, message) {
  const enc = new TextEncoder();
  const cryptoKey = await crypto.subtle.importKey(
    "raw", enc.encode(key), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]
  );
  const sig = await crypto.subtle.sign("HMAC", cryptoKey, enc.encode(message));
  return [...new Uint8Array(sig)].map((b) => b.toString(16).padStart(2, "0")).join("");
}

async function makeCookie(payload, ttlSeconds, secret) {
  const full = { ...payload, exp: Date.now() + ttlSeconds * 1000 };
  const encoded = b64urlEncode(JSON.stringify(full));
  const sig = await hmac(secret, encoded);
  return `${encoded}.${sig}`;
}

async function verifyCookie(value, secret) {
  if (!value) return null;
  const dot = value.indexOf(".");
  if (dot === -1) return null;
  const encoded = value.slice(0, dot);
  const sig = value.slice(dot + 1);
  const expected = await hmac(secret, encoded);
  if (expected !== sig) return null;
  try {
    const payload = JSON.parse(b64urlDecode(encoded));
    if (!payload.exp || payload.exp < Date.now()) return null;
    return payload;
  } catch {
    return null;
  }
}

function getCookie(request, name) {
  const header = request.headers.get("Cookie") || "";
  for (const part of header.split(";")) {
    const eq = part.indexOf("=");
    if (eq === -1) continue;
    const key = part.slice(0, eq).trim();
    if (key === name) return decodeURIComponent(part.slice(eq + 1).trim());
  }
  return null;
}

function escapeHtml(str) {
  return String(str).replace(/[&<>"']/g, (c) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
  }[c]));
}

async function getCredentialsForSlug(env, slug) {
  const val = await env.DRAFT_CREDENTIALS.get(slug, { type: "json" });
  return Array.isArray(val) ? val : [];
}

async function getAdminCredential(env) {
  return await env.DRAFT_CREDENTIALS.get("_admin", { type: "json" });
}

async function findMatch(env, slug, email, password) {
  const admin = await getAdminCredential(env);
  if (admin && admin.email === email && admin.password === password) {
    return { scope: "*", email };
  }
  const creds = await getCredentialsForSlug(env, slug);
  const idx = creds.findIndex((c) => c.email === email && c.password === password);
  if (idx !== -1) {
    return { scope: slug, email, mustReset: !!creds[idx].mustReset, creds, idx };
  }
  return null;
}

function pageShell(title, bodyHtml) {
  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${escapeHtml(title)} — Tekton by Bigie</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
  :root{--accent:#C97A3E;--ink:#F5F3EE;--panel:#121316;}
  *{box-sizing:border-box;}
  html,body{margin:0;min-height:100vh;background:var(--panel);color:var(--ink);font-family:'Space Grotesk',sans-serif;
    display:flex;align-items:center;justify-content:center;padding:24px;}
  .card{width:100%;max-width:380px;background:linear-gradient(180deg,#1D1F23 0%,#17191C 100%);
    border:1px solid #2C2E33;border-radius:10px;padding:36px 32px;box-shadow:0 12px 32px rgba(0,0,0,0.4);}
  .brand{font-family:'IBM Plex Mono',monospace;font-size:0.68rem;letter-spacing:0.15em;color:#8B8D94;
    text-transform:uppercase;margin-bottom:18px;}
  h1{font-size:1.3rem;margin:0 0 22px 0;}
  label{display:block;font-family:'IBM Plex Mono',monospace;font-size:0.7rem;letter-spacing:0.06em;
    text-transform:uppercase;color:#8B8D94;margin-bottom:6px;}
  input{width:100%;padding:11px 12px;margin-bottom:18px;background:#0F1012;border:1px solid #2C2E33;
    border-radius:5px;color:var(--ink);font-family:'Space Grotesk',sans-serif;font-size:0.95rem;}
  input:focus{outline:none;border-color:var(--accent);}
  button{width:100%;padding:12px;background:var(--accent);border:none;border-radius:5px;color:#121316;
    font-family:'IBM Plex Mono',monospace;font-size:0.78rem;letter-spacing:0.05em;text-transform:uppercase;
    font-weight:600;cursor:pointer;}
  .error{background:rgba(201,60,60,0.12);border:1px solid rgba(201,60,60,0.4);color:#E88;
    padding:10px 12px;border-radius:5px;font-size:0.85rem;margin-bottom:18px;}
  .hint{font-family:'IBM Plex Mono',monospace;font-size:0.72rem;color:#6C6E75;margin-top:16px;line-height:1.6;}
</style>
</head>
<body>
<div class="card">
  <div class="brand">Tekton by Bigie</div>
  ${bodyHtml}
</div>
</body>
</html>`;
}

function loginPage({ slug, isAdmin, error }) {
  const heading = isAdmin ? "Admin Login" : "Draft Preview Login";
  return pageShell(heading, `
    <h1>${escapeHtml(heading)}</h1>
    ${error ? `<div class="error">${escapeHtml(error)}</div>` : ""}
    <form method="POST">
      <label for="email">Email</label>
      <input id="email" name="email" type="email" autocomplete="username" required autofocus>
      <label for="password">Password</label>
      <input id="password" name="password" type="password" autocomplete="current-password" required>
      <button type="submit">Log In</button>
    </form>
    <div class="hint">Internal review only &mdash; not public.</div>
    <script>
      var e=document.getElementById('email'), p=document.getElementById('password');
      e.addEventListener('keydown', function(ev){
        if(ev.key==='Enter'){ ev.preventDefault(); p.focus(); }
      });
    </script>
  `);
}

function resetPage({ slug, email, error }) {
  return pageShell("Set a New Password", `
    <h1>Set a New Password</h1>
    ${error ? `<div class="error">${escapeHtml(error)}</div>` : ""}
    <form method="POST">
      <input type="hidden" name="action" value="set_password">
      <label>Email</label>
      <input type="email" value="${escapeHtml(email)}" disabled>
      <label for="new_password">New Password</label>
      <input id="new_password" name="new_password" type="password" autocomplete="new-password" required minlength="6" autofocus>
      <label for="confirm_password">Confirm Password</label>
      <input id="confirm_password" name="confirm_password" type="password" autocomplete="new-password" required minlength="6">
      <button type="submit">Set Password &amp; Continue</button>
    </form>
    <div class="hint">You're using a temporary password &mdash; pick your own to continue.</div>
    <script>
      var n=document.getElementById('new_password'), c=document.getElementById('confirm_password');
      n.addEventListener('keydown', function(ev){
        if(ev.key==='Enter'){ ev.preventDefault(); c.focus(); }
      });
    </script>
  `);
}

function htmlResponse(html, status, setCookies) {
  const headers = new Headers({ "Content-Type": "text/html; charset=utf-8", "Cache-Control": "no-store" });
  for (const c of setCookies || []) headers.append("Set-Cookie", c);
  return new Response(html, { status: status || 200, headers });
}

function redirect(location, setCookies) {
  const headers = new Headers({ Location: location });
  for (const c of setCookies || []) headers.append("Set-Cookie", c);
  return new Response(null, { status: 303, headers });
}

async function renderAdminPage(env) {
  const list = await env.DRAFT_CREDENTIALS.list();
  const rows = [];
  for (const key of list.keys) {
    if (key.name === "_admin") continue;
    const val = await env.DRAFT_CREDENTIALS.get(key.name, { type: "json" });
    const creds = Array.isArray(val) ? val : [];
    rows.push({ slug: key.name, creds });
  }
  const tableRows = rows.map((r) => `
    <tr>
      <td>${escapeHtml(r.slug)}</td>
      <td>${r.creds.length === 0 ? '<span class="muted">none</span>' : r.creds.map((c) =>
        `${escapeHtml(c.email)} / <code>${escapeHtml(c.password)}</code>${c.mustReset ? ' <span class="pending">(temp, needs reset)</span>' : ""}`
      ).join("<br>")}</td>
    </tr>`).join("");

  return htmlResponse(`<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Admin — Tekton by Bigie</title>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
  :root{--accent:#C97A3E;--ink:#F5F3EE;--panel:#121316;}
  *{box-sizing:border-box;}
  html,body{margin:0;background:var(--panel);color:var(--ink);font-family:'Space Grotesk',sans-serif;padding:40px 5vw;}
  h1{font-size:1.6rem;margin:0 0 24px 0;}
  table{width:100%;border-collapse:collapse;font-size:0.9rem;}
  th,td{text-align:left;padding:12px 14px;border-bottom:1px solid #2C2E33;vertical-align:top;}
  th{font-family:'IBM Plex Mono',monospace;font-size:0.68rem;letter-spacing:0.08em;text-transform:uppercase;color:#8B8D94;}
  code{background:#0F1012;padding:2px 6px;border-radius:3px;font-family:'IBM Plex Mono',monospace;}
  .muted{color:#5A5D63;}
  .pending{color:var(--accent);font-family:'IBM Plex Mono',monospace;font-size:0.72rem;}
  .hint{font-family:'IBM Plex Mono',monospace;font-size:0.72rem;color:#6C6E75;margin-top:24px;line-height:1.7;}
  code.cmd{display:block;background:#0F1012;padding:10px 12px;border-radius:5px;margin-top:6px;overflow-x:auto;}
</style>
</head>
<body>
  <h1>Draft Access — All Clients</h1>
  <table>
    <tr><th>Client</th><th>Logins</th></tr>
    ${tableRows || '<tr><td colspan="2" class="muted">No client credentials set yet.</td></tr>'}
  </table>
  <div class="hint">
    To add or update a client's login:<br>
    <code class="cmd">npx wrangler kv key put --binding=DRAFT_CREDENTIALS "&lt;slug&gt;" '[{"email":"person@example.com","password":"temp-password","mustReset":true}]'</code>
  </div>
</body>
</html>`, 200, []);
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const segments = url.pathname.split("/").filter(Boolean);
    const isAdminRoute = segments[0] === "admin";
    const isDraft = segments.includes("draft");

    if (!isDraft && !isAdminRoute) {
      return env.ASSETS.fetch(request);
    }

    const slug = isAdminRoute ? "_admin" : segments[0];
    const secret = env.SESSION_SECRET;
    if (!secret) {
      return htmlResponse(pageShell("Unavailable", "<h1>Not configured</h1><p>Session secret is missing.</p>"), 503, []);
    }

    const session = await verifyCookie(getCookie(request, SESSION_COOKIE), secret);
    const authorized = session && (session.scope === "*" || session.scope === slug);

    if (authorized) {
      if (isAdminRoute) return renderAdminPage(env);
      return env.ASSETS.fetch(request);
    }

    if (request.method === "POST") {
      const form = await request.formData();
      const action = form.get("action");

      if (action === "set_password") {
        const resetPayload = await verifyCookie(getCookie(request, RESET_COOKIE), secret);
        if (!resetPayload || resetPayload.scope !== slug) {
          return htmlResponse(loginPage({ slug, isAdmin: isAdminRoute, error: "That reset link expired. Log in again." }), 401, []);
        }
        const newPassword = String(form.get("new_password") || "");
        const confirmPassword = String(form.get("confirm_password") || "");
        if (newPassword.length < 6) {
          return htmlResponse(resetPage({ slug, email: resetPayload.email, error: "Password must be at least 6 characters." }), 400, []);
        }
        if (newPassword !== confirmPassword) {
          return htmlResponse(resetPage({ slug, email: resetPayload.email, error: "Passwords don't match." }), 400, []);
        }
        const creds = await getCredentialsForSlug(env, slug);
        const idx = creds.findIndex((c) => c.email === resetPayload.email);
        if (idx === -1) {
          return htmlResponse(loginPage({ slug, isAdmin: isAdminRoute, error: "Account not found. Log in again." }), 400, []);
        }
        creds[idx] = { email: creds[idx].email, password: newPassword, mustReset: false };
        await env.DRAFT_CREDENTIALS.put(slug, JSON.stringify(creds));
        const cookie = await makeCookie({ scope: slug, email: resetPayload.email }, SESSION_TTL_SECONDS, secret);
        return redirect(url.pathname, [
          `${SESSION_COOKIE}=${cookie}; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=${SESSION_TTL_SECONDS}`,
          `${RESET_COOKIE}=; Path=/; Max-Age=0`,
        ]);
      }

      const email = String(form.get("email") || "").trim();
      const password = String(form.get("password") || "");
      const match = await findMatch(env, slug, email, password);

      if (!match) {
        return htmlResponse(loginPage({ slug, isAdmin: isAdminRoute, error: "Invalid email or password." }), 401, []);
      }

      if (match.mustReset) {
        const resetCookie = await makeCookie({ scope: slug, email }, RESET_TTL_SECONDS, secret);
        return htmlResponse(resetPage({ slug, email }), 200, [
          `${RESET_COOKIE}=${resetCookie}; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=${RESET_TTL_SECONDS}`,
        ]);
      }

      const cookie = await makeCookie({ scope: match.scope, email }, SESSION_TTL_SECONDS, secret);
      return redirect(url.pathname, [
        `${SESSION_COOKIE}=${cookie}; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=${SESSION_TTL_SECONDS}`,
      ]);
    }

    return htmlResponse(loginPage({ slug, isAdmin: isAdminRoute }), 401, []);
  },
};
