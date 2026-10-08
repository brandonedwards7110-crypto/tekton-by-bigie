const SESSION_COOKIE = "tekton_auth";
const RESET_COOKIE = "tekton_reset";
const ME_COOKIE = "tekton_me"; // set on any device where the admin has logged in; its visits aren't counted as client activity
const ME_TTL_SECONDS = 60 * 60 * 24 * 365;
const SESSION_TTL_SECONDS = 60 * 60 * 24 * 30; // 30 days
const RESET_TTL_SECONDS = 60 * 10; // 10 minutes to finish a password reset
const RESET_LINK_TTL_SECONDS = 60 * 30; // emailed "forgot password" links work once, for 30 minutes
const SITE_ORIGIN = "https://tektonbybigie.com";
const MAIL_FROM = "no-reply@tektonbybigie.com";

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

// Viewers (KV key "_viewers": [{"email","password"}]): people Brandon sets up who can open EVERY draft but not /admin.
// Their visits are never logged as client activity and their devices get the same "ignore me" cookie as the admin's.
async function getViewers(env) {
  const val = await env.DRAFT_CREDENTIALS.get("_viewers", { type: "json" });
  return Array.isArray(val) ? val : [];
}

// ---- password storage + login lockout ----
// Temp passwords Brandon hands out stay readable (he has to send them). Anything an owner (or the admin) sets
// themselves is stored only as a salted PBKDF2 hash, never as text. Logins lock after repeated wrong tries.
const PBKDF2_ITER = 100000;
const LOCK_MAX_FAILS = 5;
const LOCK_SECONDS = 15 * 60;

function bytesToHex(buf) { return [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, "0")).join(""); }
function hexToBytes(hex) {
  const out = new Uint8Array(hex.length / 2);
  for (let i = 0; i < out.length; i++) out[i] = parseInt(hex.substr(i * 2, 2), 16);
  return out;
}
async function pbkdf2Hex(password, saltHex, iter) {
  const key = await crypto.subtle.importKey("raw", new TextEncoder().encode(password), "PBKDF2", false, ["deriveBits"]);
  const bits = await crypto.subtle.deriveBits({ name: "PBKDF2", hash: "SHA-256", salt: hexToBytes(saltHex), iterations: iter }, key, 256);
  return bytesToHex(bits);
}
function safeEqual(a, b) {
  a = String(a); b = String(b);
  let diff = a.length ^ b.length;
  const n = Math.max(a.length, b.length);
  for (let i = 0; i < n; i++) diff |= (a.charCodeAt(i) || 0) ^ (b.charCodeAt(i) || 0);
  return diff === 0;
}
async function newPasswordRecord(password) {
  const salt = bytesToHex(crypto.getRandomValues(new Uint8Array(16)));
  return { hash: await pbkdf2Hex(password, salt, PBKDF2_ITER), salt, iter: PBKDF2_ITER };
}
async function passwordMatches(cred, password) {
  if (!cred) return false;
  if (cred.hash && cred.salt) return safeEqual(await pbkdf2Hex(password, cred.salt, cred.iter || PBKDF2_ITER), cred.hash);
  if (typeof cred.password === "string") return safeEqual(cred.password, password);
  return false;
}
function clientIp(request) { return request.headers.get("CF-Connecting-IP") || "unknown"; }

// One tiny Durable Object per (login page + visitor IP) counts attempts exactly (KV can serve stale values, so it
// can't be used for this). Each attempt is counted BEFORE the password is checked, so a burst of parallel guesses
// can't slip through; a correct login resets the count. If the guard is ever unavailable we fail open (log in
// normally) rather than lock Brandon out of his own admin.
async function guardCall(env, slug, request, action) {
  try {
    if (!env.LOGIN_GUARD) return { locked: false };
    const stub = env.LOGIN_GUARD.get(env.LOGIN_GUARD.idFromName(slug + ":" + clientIp(request)));
    const r = await stub.fetch("https://guard/" + action);
    return await r.json();
  } catch (e) {
    return { locked: false };
  }
}

// ---- "Forgot password" by email ----
// A reset link is a random 256-bit token. Only its SHA-256 lives server-side, inside a Durable Object named after it
// (strongly consistent, so the link really works once; KV could serve a stale copy). Requests to send a link are
// throttled per email address and per visitor IP so nobody can use the form to flood an owner's inbox.
async function sha256Hex(s) {
  return bytesToHex(await crypto.subtle.digest("SHA-256", new TextEncoder().encode(s)));
}
function guardStub(env, name) { return env.LOGIN_GUARD.get(env.LOGIN_GUARD.idFromName(name)); }

// Fails CLOSED: if the throttle can't be reached we don't send mail.
async function forgotAllowed(env, name, max, windowSeconds) {
  try {
    const r = await guardStub(env, name).fetch(`https://guard/forgot_hit?max=${max}&window=${windowSeconds}`);
    return (await r.json()).allowed === true;
  } catch (e) {
    return false;
  }
}

async function resetTokenCall(env, token, action, body) {
  const stub = guardStub(env, "reset:" + (await sha256Hex(token)));
  const r = await stub.fetch("https://guard/" + action, body ? { method: "POST", body: JSON.stringify(body) } : undefined);
  return await r.json();
}
async function peekResetToken(env, token) {
  try { return token ? await resetTokenCall(env, token, "reset_peek") : { valid: false }; } catch (e) { return { valid: false }; }
}
async function takeResetToken(env, token) {
  try { return token ? await resetTokenCall(env, token, "reset_take") : { valid: false }; } catch (e) { return { valid: false }; }
}

async function sendResetEmail(env, to, link) {
  const mins = RESET_LINK_TTL_SECONDS / 60;
  const text = `Someone asked to reset the password for your Tekton by Bigie draft preview.\n\n` +
    `Set a new password here (the link works once and expires in ${mins} minutes):\n${link}\n\n` +
    `If you didn't ask for this, ignore this email. Your password stays the same.\n\n— Tekton by Bigie`;
  const html = `<div style="font-family:Arial,Helvetica,sans-serif;font-size:15px;line-height:1.5;color:#222;max-width:480px">` +
    `<p>Someone asked to reset the password for your Tekton by Bigie draft preview.</p>` +
    `<p><a href="${escapeHtml(link)}" style="display:inline-block;background:#C97A3E;color:#121316;text-decoration:none;font-weight:bold;padding:12px 20px;border-radius:5px">Set a new password</a></p>` +
    `<p style="color:#555;font-size:13px">The link works once and expires in ${mins} minutes. If the button doesn't work, paste this into your browser:<br>${escapeHtml(link)}</p>` +
    `<p style="color:#555;font-size:13px">If you didn't ask for this, ignore this email. Your password stays the same.</p>` +
    `<p style="color:#888;font-size:12px">Tekton by Bigie</p></div>`;
  return env.EMAIL.send({ from: MAIL_FROM, to, subject: "Reset your password — Tekton by Bigie", html, text });
}

// Runs after the response is already sent, so a real address and an unknown one look identical (no guessing who has access).
async function processForgotRequest(env, request, slug, pathname, emailInput) {
  try {
    if (!env.EMAIL || !env.LOGIN_GUARD) return;
    const email = String(emailInput || "").trim().toLowerCase().slice(0, 120);
    if (!email.includes("@")) return;
    if (!(await forgotAllowed(env, "forgotip:" + clientIp(request), 10, 3600))) return;
    const creds = await getCredentialsForSlug(env, slug);
    let cred = creds.find((c) => String(c.email || "").toLowerCase() === email);
    let viewer = false;
    if (!cred) {   // viewers can reset from any draft's login page; it changes the viewer login, never a client's
      cred = (await getViewers(env)).find((v) => String(v.email || "").toLowerCase() === email);
      viewer = !!cred;
    }
    if (!cred) return;
    if (!(await forgotAllowed(env, "forgot:" + (viewer ? "viewer" : slug) + ":" + email, 3, 3600))) return;
    const token = bytesToHex(crypto.getRandomValues(new Uint8Array(32)));
    await resetTokenCall(env, token, "reset_put", { slug, email: cred.email, viewer, exp: Date.now() + RESET_LINK_TTL_SECONDS * 1000 });
    const link = `${SITE_ORIGIN}${pathname}?reset=${token}`;
    await sendResetEmail(env, cred.email, link);
    if (!viewer) await logActivity(env, slug, "reset_requested", { email: cred.email, request });
  } catch (e) {
    console.error("forgot-password email failed:", e && e.code, e && e.message);
  }
}

export class LoginGuard {
  constructor(state) { this.state = state; }
  async alarm() { await this.state.storage.deleteAll(); } // expired reset tokens / throttle counters clean themselves up
  async handleForgot(action, request, now) {
    const json = (o) => new Response(JSON.stringify(o), { headers: { "content-type": "application/json" } });
    const url = new URL(request.url);
    if (action === "forgot_hit") {
      const max = Number(url.searchParams.get("max")) || 3;
      const windowMs = (Number(url.searchParams.get("window")) || 3600) * 1000;
      const hits = ((await this.state.storage.get("hits")) || []).filter((t) => now - t < windowMs);
      const allowed = hits.length < max;
      if (allowed) hits.push(now);
      await this.state.storage.put("hits", hits);
      await this.state.storage.setAlarm(now + windowMs + 1000);
      return json({ allowed });
    }
    if (action === "reset_put") {
      const rec = await request.json();
      await this.state.storage.put("reset", rec);
      await this.state.storage.setAlarm(rec.exp + 1000);
      return json({ ok: true });
    }
    const rec = await this.state.storage.get("reset");
    if (!rec || rec.exp < now) { await this.state.storage.deleteAll(); return json({ valid: false }); }
    if (action === "reset_take") await this.state.storage.deleteAll(); // single use
    return json({ valid: true, slug: rec.slug, email: rec.email, viewer: !!rec.viewer });
  }
  async fetch(request) {
    const action = new URL(request.url).pathname.slice(1);
    const now = Date.now();
    if (action === "forgot_hit" || action.startsWith("reset_")) return this.handleForgot(action, request, now);
    let rec = (await this.state.storage.get("rec")) || { fails: 0, lockedUntil: 0, last: 0 };
    if (rec.lockedUntil && now >= rec.lockedUntil) rec = { fails: 0, lockedUntil: 0, last: 0 };
    if (!rec.lockedUntil && rec.fails && now - rec.last > LOCK_SECONDS * 1000) rec = { fails: 0, lockedUntil: 0, last: 0 };
    let locked = false;
    if (action === "attempt") {
      if (rec.lockedUntil && now < rec.lockedUntil) {
        locked = true;
      } else {
        rec.fails += 1;
        rec.last = now;
        if (rec.fails > LOCK_MAX_FAILS) { rec.lockedUntil = now + LOCK_SECONDS * 1000; locked = true; }
        await this.state.storage.put("rec", rec);
      }
    } else if (action === "ok") {
      await this.state.storage.delete("rec");
      rec = { fails: 0, lockedUntil: 0, last: 0 };
    }
    return new Response(JSON.stringify({ locked, fails: rec.fails, retryAfterSeconds: locked ? Math.ceil((rec.lockedUntil - now) / 1000) : 0 }),
      { headers: { "content-type": "application/json" } });
  }
}

// ---- client activity tracking (shown on /admin) ----
const ACTIVITY_PREFIX = "_activity:";
const MAX_EVENTS = 60;
const VIEW_THROTTLE_MS = 10 * 60 * 1000;
const DUPE_WINDOW_MS = 3 * 60 * 1000;
const TRACKED_CLIENT_TYPES = ["view", "temp_login", "login", "password_set"];

function isBotUA(ua) {
  return !ua || /bot|crawl|spider|preview|facebookexternalhit|slurp|whatsapp|telegram|discord|skype|embedly|curl|wget|python|go-http|okhttp|headless|lighthouse|monitor|uptime|node-fetch|axios|tektoncheck/i.test(ua)   // 'TektonCheck' = Claude's own site tests, never counted as client activity;
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
    if (getCookie(request, ME_COOKIE) === "1") return;
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
        if (type === "login" || type === "temp_login") {
          c.firstLoginAt = c.firstLoginAt || now;
          c.loginCount = (c.loginCount || 0) + 1;
        }
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
  temp_login: "Logged in",
  password_set: "Changed their password",
  reset_requested: "Asked for a password reset email",
  login: "Logged in",
  view: "Viewed the draft",
};

async function findMatch(env, slug, email, password) {
  const admin = await getAdminCredential(env);
  if (admin && admin.email === email && (await passwordMatches(admin, password))) {
    return { scope: "*", email };
  }
  for (const v of await getViewers(env)) {
    if (v.email === email && (await passwordMatches(v, password))) return { scope: "viewer", email };
  }
  const creds = await getCredentialsForSlug(env, slug);
  for (let idx = 0; idx < creds.length; idx++) {
    if (creds[idx].email === email && (await passwordMatches(creds[idx], password))) {
      return { scope: slug, email, mustReset: !!creds[idx].mustReset, creds, idx };
    }
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
  label.chk{display:flex;align-items:center;gap:8px;margin:-6px 0 18px 0;text-transform:none;letter-spacing:0.02em;font-size:0.74rem;cursor:pointer;}
  label.chk input{width:auto;margin:0;}
  button{width:100%;padding:12px;background:var(--accent);border:none;border-radius:5px;color:#121316;
    font-family:'IBM Plex Mono',monospace;font-size:0.78rem;letter-spacing:0.05em;text-transform:uppercase;
    font-weight:600;cursor:pointer;}
  .error{background:rgba(201,60,60,0.12);border:1px solid rgba(201,60,60,0.4);color:#E88;
    padding:10px 12px;border-radius:5px;font-size:0.85rem;margin-bottom:18px;}
  .hint{font-family:'IBM Plex Mono',monospace;font-size:0.72rem;color:#6C6E75;margin-top:16px;line-height:1.6;}
  .hint a{color:var(--accent);}
  .ok{background:rgba(80,170,110,0.12);border:1px solid rgba(80,170,110,0.4);color:#9ED8B0;
    padding:10px 12px;border-radius:5px;font-size:0.85rem;margin-bottom:18px;line-height:1.5;}
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
      <label class="chk"><input type="checkbox" id="showpw"> Show password</label>
      ${isAdmin ? "" : '<label class="chk"><input type="checkbox" name="change_password" value="1"> Change my password</label>'}
      <button type="submit">Log In</button>
    </form>
    ${isAdmin ? "" : '<div class="hint"><a href="?forgot=1">Forgot password?</a></div>'}
    <div class="hint">Internal review only &mdash; not public.</div>
    <script>
      var e=document.getElementById('email'), p=document.getElementById('password');
      e.addEventListener('keydown', function(ev){
        if(ev.key==='Enter'){ ev.preventDefault(); p.focus(); }
      });
      document.getElementById('showpw').addEventListener('change', function(){
        p.type = this.checked ? 'text' : 'password';
      });
    </script>
  `);
}

function forgotPage({ error }) {
  return pageShell("Forgot Password", `
    <h1>Forgot your password?</h1>
    ${error ? `<div class="error">${escapeHtml(error)}</div>` : ""}
    <form method="POST">
      <input type="hidden" name="action" value="forgot">
      <label for="email">Your email</label>
      <input id="email" name="email" type="email" autocomplete="username" required autofocus>
      <button type="submit">Email Me a Reset Link</button>
    </form>
    <div class="hint"><a href="./">Back to log in</a></div>
  `);
}

function forgotSentPage() {
  return pageShell("Check Your Email", `
    <h1>Check your email</h1>
    <div class="ok">If that address has access to this preview, a reset link is on its way. It can take a minute &mdash; check your spam folder too. The link works once and expires in ${RESET_LINK_TTL_SECONDS / 60} minutes.</div>
    <div class="hint"><a href="./">Back to log in</a></div>
  `);
}

// token is set when the owner arrived from an emailed reset link; otherwise this is the signed-cookie flow (temp password / "Change my password").
function resetPage({ slug, email, error, token }) {
  return pageShell("Set a New Password", `
    <h1>Set a New Password</h1>
    ${error ? `<div class="error">${escapeHtml(error)}</div>` : ""}
    <form method="POST">
      <input type="hidden" name="action" value="${token ? "reset_with_token" : "set_password"}">
      ${token ? `<input type="hidden" name="token" value="${escapeHtml(token)}">` : ""}
      <label>Email</label>
      <input type="email" value="${escapeHtml(email)}" disabled>
      <label for="new_password">New Password</label>
      <input id="new_password" name="new_password" type="password" autocomplete="new-password" required minlength="6" autofocus>
      <label for="confirm_password">Confirm Password</label>
      <input id="confirm_password" name="confirm_password" type="password" autocomplete="new-password" required minlength="6">
      <label class="chk"><input type="checkbox" id="showpw"> Show passwords</label>
      <button type="submit">Set Password &amp; Continue</button>
    </form>
    <div class="hint">Pick a new password to continue &mdash; you'll use it next time you log in.</div>
    <script>
      var n=document.getElementById('new_password'), c=document.getElementById('confirm_password');
      n.addEventListener('keydown', function(ev){
        if(ev.key==='Enter'){ ev.preventDefault(); c.focus(); }
      });
      document.getElementById('showpw').addEventListener('change', function(){
        n.type = c.type = this.checked ? 'text' : 'password';
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

const ME_COOKIE_VALUE = `${ME_COOKIE}=1; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=${ME_TTL_SECONDS}`;

function withMeCookie(response, request, session) {
  if (!session || (session.scope !== "*" && session.scope !== "viewer") || getCookie(request, ME_COOKIE) === "1") return response;
  const r = new Response(response.body, response);
  r.headers.append("Set-Cookie", ME_COOKIE_VALUE);
  return r;
}

async function renderAdminPage(env) {
  const list = await env.DRAFT_CREDENTIALS.list();
  const rows = [];
  for (const key of list.keys) {
    if (key.name.startsWith("_")) continue;   // _admin, _activity:*, _fail:* are internal
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
      if (a.lastLoginAt) {
        badge = `<span class="st ok">Logged in ${escapeHtml(ago(a.lastLoginAt))}</span>`;
      } else if (a.priorLogin) {
        badge = '<span class="st ok">Logged in (time not recorded)</span>';
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
        `${escapeHtml(c.email)} / ${c.hash ? '<span class="pending">(changed by owner &mdash; not shown)</span>' : "<code>" + escapeHtml(c.password || "") + "</code>"}${c.mustReset ? ' <span class="pending">(temp, needs reset)</span>' : ""}`
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
    Activity tracking began 2026-10-02 &mdash; earlier visits weren't recorded. Times are Central. Any phone or computer where you've logged in as admin is ignored automatically (log in with your admin email once on each device, then test freely). Bots/link-preview crawlers are filtered out too. This page can lag up to a minute behind real activity.
  </div>
  <div class="hint">
    To add or update a client's login (simple passwords are fine &mdash; add <code>"mustReset":true</code> only if you ever want to force a change):<br>
    <code class="cmd">npx wrangler kv key put --binding=DRAFT_CREDENTIALS "&lt;slug&gt;" '[{"email":"person@example.com","password":"easy-password"}]'</code>
    Clients can pick their own password anytime by ticking "Change my password" on the login screen.
  </div>
  <div class="hint">
    Viewers (people who can open every draft but not this page; their visits are never counted as client activity): list them all in one key, replacing the whole list each time:<br>
    <code class="cmd">npx wrangler kv key put --binding=DRAFT_CREDENTIALS --remote "_viewers" '[{"email":"person@example.com","password":"easy-password"}]'</code>
  </div>
</body>
</html>`, 200, []);
}

// Security: always use HTTPS, and add standard protective headers to every response.
const SECURITY_HEADERS = {
  "Strict-Transport-Security": "max-age=31536000",
  "X-Content-Type-Options": "nosniff",
  "Referrer-Policy": "strict-origin-when-cross-origin",
  "X-Frame-Options": "SAMEORIGIN",
};

function withSecurityHeaders(response) {
  const r = new Response(response.body, response);
  for (const [k, v] of Object.entries(SECURITY_HEADERS)) r.headers.set(k, v);
  return r;
}

async function handleRequest(request, env, ctx) {
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
    const authorized = session && (session.scope === "*" || session.scope === slug || (session.scope === "viewer" && !isAdminRoute));

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
        return withMeCookie(await renderAdminPage(env), request, session);
      }
      if (session.scope === slug && request.method === "GET" && isHtmlNavigation(request, url)) {
        ctx.waitUntil(logActivity(env, slug, "view", { email: session.email, request }));
      }
      return withMeCookie(await env.ASSETS.fetch(request), request, session);
    }

    if (request.method === "POST") {
      const form = await request.formData();
      const action = form.get("action");

      if (action === "forgot" && !isAdminRoute) {
        // Same answer whether or not the address has access; the work happens after we respond.
        ctx.waitUntil(processForgotRequest(env, request, slug, url.pathname, form.get("email")));
        return htmlResponse(forgotSentPage(), 200, []);
      }

      if (action === "reset_with_token" && !isAdminRoute) {
        const token = String(form.get("token") || "");
        const expired = () => htmlResponse(loginPage({ slug, isAdmin: false, error: "That reset link expired or was already used. Tap \"Forgot password?\" to get a new one." }), 401, []);
        const info = await peekResetToken(env, token);
        if (!info.valid || info.slug !== slug) return expired();
        const newPassword = String(form.get("new_password") || "");
        const confirmPassword = String(form.get("confirm_password") || "");
        if (newPassword.length < 6) {
          return htmlResponse(resetPage({ slug, email: info.email, token, error: "Password must be at least 6 characters." }), 400, []);
        }
        if (newPassword !== confirmPassword) {
          return htmlResponse(resetPage({ slug, email: info.email, token, error: "Passwords don't match." }), 400, []);
        }
        const taken = await takeResetToken(env, token); // single use: only one request can win this
        if (!taken.valid || taken.slug !== slug) return expired();
        if (taken.viewer) {   // a viewer's reset: update the viewer list (scrambled), keep them out of every client's activity log
          const viewers = await getViewers(env);
          const vi = viewers.findIndex((v) => v.email === info.email);
          if (vi === -1) {
            return htmlResponse(loginPage({ slug, isAdmin: false, error: "Account not found. Ask Brandon for help." }), 400, []);
          }
          viewers[vi] = { email: viewers[vi].email, ...(await newPasswordRecord(newPassword)), changedByOwner: true, changedAt: Date.now() };
          await env.DRAFT_CREDENTIALS.put("_viewers", JSON.stringify(viewers));
          ctx.waitUntil(guardCall(env, slug, request, "ok"));
          const vcookie = await makeCookie({ scope: "viewer", email: info.email }, SESSION_TTL_SECONDS, secret);
          return redirect(url.pathname, [`${SESSION_COOKIE}=${vcookie}; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=${SESSION_TTL_SECONDS}`, ME_COOKIE_VALUE]);
        }
        const creds = await getCredentialsForSlug(env, slug);
        const idx = creds.findIndex((c) => c.email === info.email);
        if (idx === -1) {
          return htmlResponse(loginPage({ slug, isAdmin: false, error: "Account not found. Ask Brandon for help." }), 400, []);
        }
        creds[idx] = { email: creds[idx].email, ...(await newPasswordRecord(newPassword)), mustReset: false, changedByOwner: true, changedAt: Date.now() };
        await env.DRAFT_CREDENTIALS.put(slug, JSON.stringify(creds));
        ctx.waitUntil(guardCall(env, slug, request, "ok"));
        ctx.waitUntil(logActivity(env, slug, "password_set", { email: info.email, request }));
        const cookie = await makeCookie({ scope: slug, email: info.email }, SESSION_TTL_SECONDS, secret);
        return redirect(url.pathname, [`${SESSION_COOKIE}=${cookie}; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=${SESSION_TTL_SECONDS}`]);
      }

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
        creds[idx] = { email: creds[idx].email, ...(await newPasswordRecord(newPassword)), mustReset: false, changedByOwner: true, changedAt: Date.now() };
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
      const guard = await guardCall(env, slug, request, "attempt");
      if (guard.locked) {
        return htmlResponse(loginPage({ slug, isAdmin: isAdminRoute, error: "Too many wrong tries. Please wait 15 minutes, then try again." }), 429, []);
      }
      let match = await findMatch(env, slug, email, password);
      if (match && match.scope === "viewer" && isAdminRoute) match = null;   // viewers can never log in to /admin

      if (!match) {
        if (!isAdminRoute) ctx.waitUntil(logActivity(env, slug, "failed_login", { email, request }));
        return htmlResponse(loginPage({ slug, isAdmin: isAdminRoute, error: "Invalid email or password." }), 401, []);
      }

      ctx.waitUntil(guardCall(env, slug, request, "ok"));
      if (!isAdminRoute && match.scope === slug) {
        ctx.waitUntil(logActivity(env, slug, "login", { email, request }));
      }

      const wantsChange = form.get("change_password") === "1";
      if (match.scope !== "*" && match.scope !== "viewer" && (match.mustReset || wantsChange)) {
        const resetCookie = await makeCookie({ scope: slug, email }, RESET_TTL_SECONDS, secret);
        return htmlResponse(resetPage({ slug, email }), 200, [
          `${RESET_COOKIE}=${resetCookie}; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=${RESET_TTL_SECONDS}`,
        ]);
      }

      const cookie = await makeCookie({ scope: match.scope, email }, SESSION_TTL_SECONDS, secret);
      const loginCookies = [`${SESSION_COOKIE}=${cookie}; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=${SESSION_TTL_SECONDS}`];
      if (match.scope === "*" || match.scope === "viewer") loginCookies.push(ME_COOKIE_VALUE);
      return redirect(url.pathname, loginCookies);
    }

    if (request.method === "GET" && !isAdminRoute) {
      if (url.searchParams.has("forgot")) return htmlResponse(forgotPage({}), 200, []);
      const token = url.searchParams.get("reset");
      if (token) {
        // Only looks the token up (doesn't use it up) so an email link-scanner can't burn the link before the owner clicks it.
        const info = await peekResetToken(env, token);
        if (info.valid && info.slug === slug) return htmlResponse(resetPage({ slug, email: info.email, token }), 200, []);
        return htmlResponse(loginPage({ slug, isAdmin: false, error: "That reset link expired or was already used. Tap \"Forgot password?\" to get a new one." }), 401, []);
      }
    }
    if (request.method === "GET" && !isAdminRoute && isHtmlNavigation(request, url)) {
      ctx.waitUntil(logActivity(env, slug, "link_opened", { request }));
    }
    return htmlResponse(loginPage({ slug, isAdmin: isAdminRoute }), 401, []);
}

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const isLocal = url.hostname === "localhost" || url.hostname === "127.0.0.1" || url.hostname.endsWith(".localhost");
    if (url.protocol === "http:" && !isLocal) {
      url.protocol = "https:";
      return Response.redirect(url.toString(), 301);
    }
    return withSecurityHeaders(await handleRequest(request, env, ctx));
  },
};
