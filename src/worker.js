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

// ---- client activity tracking (shown on /admin) ----
const ACTIVITY_PREFIX = "_activity:";
const MAX_EVENTS = 60;
const VIEW_THROTTLE_MS = 10 * 60 * 1000;
const DUPE_WINDOW_MS = 3 * 60 * 1000;
const TRACKED_CLIENT_TYPES = ["view", "temp_login", "login", "password_set"];

function isBotUA(ua) {
  return !ua || /bot|crawl|spider|preview|facebookexternalhit|slurp|whatsapp|telegram|discord|skype|embedly|curl|wget|python|go-http|okhttp|headless|lighthouse|monitor|uptime|node-fetch|axios/i.test(ua);
}

function describeUA(ua) {
  const os = /iPhone/.test(ua) ? "iPhone" : /iPad/.test(ua) ? "iPad" : /Android/.test(ua) ? "Android"
    : /Macintosh|Mac OS X/.test(ua) ? "Mac" : /Windows/.test(ua) ? "Windows" : /Linux/.test(ua) ? "Linux" : "Unknown device";
  const br = /Edg\//.test(ua) ? "Edge" : /OPR\/|Opera/.test(ua) ? "Opera" : /CriOS|Chrome\//.test(ua) ? "Chrome"
    : /FxiOS|Firefox\//.test(ua) ? "Firefox" : /Safari\//.test(ua) ? "Safari" : "";
  return br ? `${os} · ${br}` : os;
}

function isHtmlNavigation(request, url) {
  const dest = request.headers.get("Sec-Fetch-Dest");
  if (dest && dest !== "document") return false;
  return url.pathname.endsWith("/") || url.pathname.endsWith(".html");
}

async function logActivity(env, slug, type, { email, request }) {
  try {
    const ua = request.headers.get("User-Agent") || "";
    if (isBotUA(ua)) return;
    const creds = await getCredentialsForSlug(env, slug);
    if (!creds.length) return;

    const cf = request.cf || {};
    const loc = [cf.city, cf.region, cf.country].filter(Boolean).join(", ");
    const device = describeUA(ua);
    const cleanEmail = email ? String(email).slice(0, 80) : null;
    const key = ACTIVITY_PREFIX + slug;
    const data = (await env.DRAFT_CREDENTIALS.get(key, { type: "json" })) || {};
    data.events = Array.isArray(data.events) ? data.events : [];
    data.clients = data.clients || {};
    const now = Date.now();
    const c = cleanEmail && TRACKED_CLIENT_TYPES.includes(type)
      ? (data.clients[cleanEmail] = data.clients[cleanEmail] || {})
      : null;

    if (type === "view") {
      if (c.lastViewAt && now - c.lastViewAt < VIEW_THROTTLE_MS) return;
      c.lastViewAt = now;
      c.viewCount = (c.viewCount || 0) + 1;
    } else {
      const last = data.events[0];
      if (last && last.type === type && last.email === cleanEmail && last.device === device && last.loc === loc && now - last.t < DUPE_WINDOW_MS) return;
      if (type === "link_opened") {
        data.firstLinkOpenAt = data.firstLinkOpenAt || now;
        data.lastLinkOpenAt = now;
        data.linkOpens = (data.linkOpens || 0) + 1;
      } else if (type === "failed_login") {
        data.failedLogins = (data.failedLogins || 0) + 1;
      } else if (c) {
        if (type === "temp_login") c.firstTempLoginAt = c.firstTempLoginAt || now;
        if (type === "login") c.loginCount = (c.loginCount || 0) + 1;
        if (type === "password_set") c.passwordSetAt = now;
        c.lastLoginAt = now;
      }
    }

    data.events.unshift({ t: now, type, email: cleanEmail, device, loc });
    data.events = data.events.slice(0, MAX_EVENTS);
    await env.DRAFT_CREDENTIALS.put(key, JSON.stringify(data));
  } catch (e) {
    // tracking must never break the draft site
  }
}

const TZ = "America/Chicago";
function fmtTime(ms) {
  return new Date(ms).toLocaleString("en-US", { timeZone: TZ, month: "short", day: "numeric", hour: "numeric", minute: "2-digit" }) + " CT";
}
function ago(ms) {
  const s = Math.max(0, Math.floor((Date.now() - ms) / 1000));
  if (s < 60) return "just now";
  const m = Math.floor(s / 60);
  if (m < 60) return `${m} min ago`;
  const h = Math.floor(m / 60);
  if (h < 24) return `${h} hr ago`;
  const d = Math.floor(h / 24);
  return `${d} day${d === 1 ? "" : "s"} ago`;
}
const EVENT_LABELS = {
  link_opened: "Opened the link (saw the login page)",
  failed_login: "Failed login attempt",
  temp_login: "Logged in with the temp password",
  password_set: "Set a new password",
  login: "Logged in",
  view: "Viewed the draft",
};

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
    if (key.name === "_admin" || key.name.startsWith(ACTIVITY_PREFIX)) continue;
    const val = await env.DRAFT_CREDENTIALS.get(key.name, { type: "json" });
    const creds = Array.isArray(val) ? val : [];
    const activity = (await env.DRAFT_CREDENTIALS.get(ACTIVITY_PREFIX + key.name, { type: "json" })) || {};
    rows.push({ slug: key.name, creds, activity });
  }

  function statusCell(r) {
    if (r.creds.length === 0) return '<span class="muted">no login set</span>';
    const act = r.activity;
    return r.creds.map((c) => {
      const a = (act.clients || {})[c.email] || {};
      let badge;
      if (!c.mustReset) {
        badge = a.passwordSetAt
          ? `<span class="st ok">Password set ${escapeHtml(ago(a.passwordSetAt))}</span>`
          : '<span class="st ok">Password set (before tracking began)</span>';
      } else if (a.firstTempLoginAt) {
        badge = `<span class="st warn">Logged in with temp password ${escapeHtml(ago(a.firstTempLoginAt))} &mdash; hasn't set a new one</span>`;
      } else if (act.linkOpens) {
        badge = `<span class="st warn">Opened the link ${escapeHtml(ago(act.lastLinkOpenAt))} &mdash; hasn't logged in</span>`;
      } else {
        badge = '<span class="st none">Not opened yet</span>';
      }
      const view = a.lastViewAt
        ? `<div class="sub">Last viewed the draft ${escapeHtml(ago(a.lastViewAt))} (${a.viewCount || 1} visit${(a.viewCount || 1) === 1 ? "" : "s"})</div>`
        : "";
      return `<div class="cl"><div class="who">${escapeHtml(c.email)}</div>${badge}${view}</div>`;
    }).join("");
  }

  function activityCell(r) {
    const ev = Array.isArray(r.activity.events) ? r.activity.events : [];
    const failed = r.activity.failedLogins ? ` &middot; ${r.activity.failedLogins} failed login${r.activity.failedLogins === 1 ? "" : "s"}` : "";
    if (ev.length === 0) return '<span class="muted">no activity recorded</span>';
    const items = ev.slice(0, 15).map((e) => `
      <li><span class="when">${escapeHtml(fmtTime(e.t))}</span> <b>${escapeHtml(EVENT_LABELS[e.type] || e.type)}</b>${e.email ? ` <span class="muted">(${escapeHtml(e.email)})</span>` : ""}
        <div class="meta">${escapeHtml([e.device, e.loc].filter(Boolean).join(" · ") || "unknown")}</div></li>`).join("");
    return `<details><summary>${ev.length} event${ev.length === 1 ? "" : "s"}${failed} &mdash; last ${escapeHtml(ago(ev[0].t))}</summary><ul class="events">${items}</ul>
      <form method="POST" action="/admin" onsubmit="return confirm('Clear the activity log for ${escapeHtml(r.slug)}?')">
        <input type="hidden" name="action" value="clear_activity"><input type="hidden" name="slug" value="${escapeHtml(r.slug)}">
        <button class="clear" type="submit">Clear log</button></form></details>`;
  }

  const tableRows = rows.map((r) => `
    <tr>
      <td>${escapeHtml(r.slug)}</td>
      <td>${r.creds.length === 0 ? '<span class="muted">none</span>' : r.creds.map((c) =>
        `${escapeHtml(c.email)} / <code>${escapeHtml(c.password)}</code>${c.mustReset ? ' <span class="pending">(temp, needs reset)</span>' : ""}`
      ).join("<br>")}</td>
      <td>${statusCell(r)}</td>
      <td>${activityCell(r)}</td>
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
  .cl{margin-bottom:10px;} .cl:last-child{margin-bottom:0;}
  .who{font-size:0.78rem;color:#8B8D94;margin-bottom:3px;}
  .st{display:inline-block;font-family:'IBM Plex Mono',monospace;font-size:0.72rem;padding:4px 9px;border-radius:999px;line-height:1.4;}
  .st.ok{background:rgba(70,170,110,0.15);color:#6fd49a;border:1px solid rgba(70,170,110,0.4);}
  .st.warn{background:rgba(201,122,62,0.15);color:#E8A66A;border:1px solid rgba(201,122,62,0.45);}
  .st.none{background:rgba(255,255,255,0.05);color:#8B8D94;border:1px solid #2C2E33;}
  .sub{font-size:0.78rem;color:#9aa0a6;margin-top:5px;}
  details summary{cursor:pointer;font-size:0.84rem;color:#cfd3de;}
  ul.events{list-style:none;padding:0;margin:10px 0 8px 0;display:grid;gap:9px;font-size:0.82rem;}
  .when{font-family:'IBM Plex Mono',monospace;font-size:0.7rem;color:#8B8D94;margin-right:6px;}
  .meta{font-size:0.72rem;color:#6C6E75;margin-top:2px;}
  button.clear{background:none;border:1px solid #2C2E33;color:#8B8D94;border-radius:5px;padding:5px 10px;font-family:'IBM Plex Mono',monospace;font-size:0.68rem;cursor:pointer;}
  button.clear:hover{border-color:#a55;color:#e88;}
</style>
</head>
<body>
  <h1>Draft Access — All Clients</h1>
  <table>
    <tr><th>Client</th><th>Logins</th><th>Status</th><th>Activity</th></tr>
    ${tableRows || '<tr><td colspan="4" class="muted">No client credentials set yet.</td></tr>'}
  </table>
  <div class="hint">
    Activity tracking began 2026-10-02 &mdash; earlier visits weren't recorded. Times are Central. Your own admin views aren't counted, and bots/link-preview crawlers are filtered out. This page can lag up to a minute behind real activity.
  </div>
  <div class="hint">
    To add or update a client's login:<br>
    <code class="cmd">npx wrangler kv key put --binding=DRAFT_CREDENTIALS "&lt;slug&gt;" '[{"email":"person@example.com","password":"temp-password","mustReset":true}]'</code>
  </div>
</body>
</html>`, 200, []);
}

export default {
  async fetch(request, env, ctx) {
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
      if (isAdminRoute) {
        if (request.method === "POST") {
          const form = await request.formData();
          if (form.get("action") === "clear_activity") {
            const target = String(form.get("slug") || "");
            if (target && target !== "_admin") await env.DRAFT_CREDENTIALS.delete(ACTIVITY_PREFIX + target);
          }
          return redirect("/admin", []);
        }
        return renderAdminPage(env);
      }
      if (session.scope === slug && request.method === "GET" && isHtmlNavigation(request, url)) {
        ctx.waitUntil(logActivity(env, slug, "view", { email: session.email, request }));
      }
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
        ctx.waitUntil(logActivity(env, slug, "password_set", { email: resetPayload.email, request }));
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
        if (!isAdminRoute) ctx.waitUntil(logActivity(env, slug, "failed_login", { email, request }));
        return htmlResponse(loginPage({ slug, isAdmin: isAdminRoute, error: "Invalid email or password." }), 401, []);
      }

      if (!isAdminRoute && match.scope === slug) {
        ctx.waitUntil(logActivity(env, slug, match.mustReset ? "temp_login" : "login", { email, request }));
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

    if (request.method === "GET" && !isAdminRoute && isHtmlNavigation(request, url)) {
      ctx.waitUntil(logActivity(env, slug, "link_opened", { request }));
    }
    return htmlResponse(loginPage({ slug, isAdmin: isAdminRoute }), 401, []);
  },
};
