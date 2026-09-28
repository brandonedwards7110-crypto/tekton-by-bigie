function checkBasicAuth(request, env) {
  const expectedPass = env.DRAFTS_PASSWORD;
  if (!expectedPass) return false; // fail closed if no password is configured

  const header = request.headers.get("Authorization") || "";
  if (!header.startsWith("Basic ")) return false;

  let decoded;
  try {
    decoded = atob(header.slice(6));
  } catch {
    return false;
  }

  const sep = decoded.indexOf(":");
  if (sep === -1) return false;
  const user = decoded.slice(0, sep);
  const pass = decoded.slice(sep + 1);
  const expectedUser = env.DRAFTS_USER || "bigie";

  return user === expectedUser && pass === expectedPass;
}

function unauthorized() {
  return new Response("Authentication required", {
    status: 401,
    headers: {
      "WWW-Authenticate": 'Basic realm="Tekton by Bigie — Drafts", charset="UTF-8"',
    },
  });
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const isDraft = url.pathname.split("/").filter(Boolean).includes("draft");

    if (isDraft && !checkBasicAuth(request, env)) {
      return unauthorized();
    }

    return env.ASSETS.fetch(request);
  },
};
