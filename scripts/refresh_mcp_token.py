"""Refresh the MCP access token in .mcp.json via the OAuth proxy.

Tries the saved refresh token first. If expired, runs a full browser-based
OAuth flow to get new tokens, saves the refresh token for next time,
and updates .mcp.json with the access token.
"""

import json
import logging
import secrets
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlencode, urlparse

import requests

logger = logging.getLogger(__name__)

PROXY_BASE_URL = "https://mhi559zxqk.execute-api.us-east-1.amazonaws.com"
LOCAL_PORT = 8089
LOCAL_REDIRECT_URI = f"http://localhost:{LOCAL_PORT}/callback"
MCP_JSON_PATH = Path(__file__).resolve().parent.parent / ".mcp.json"
TOKEN_CACHE_PATH = Path(__file__).resolve().parent / ".mcp_token_cache.json"


def _load_cached_tokens() -> dict:
    if TOKEN_CACHE_PATH.exists():
        return json.loads(TOKEN_CACHE_PATH.read_text())
    return {}


def _save_cached_tokens(tokens: dict) -> None:
    TOKEN_CACHE_PATH.write_text(json.dumps(tokens, indent=2) + "\n")


def _update_mcp_json(access_token: str) -> None:
    settings = json.loads(MCP_JSON_PATH.read_text())
    settings["mcpServers"]["slack-2ndbrain-mcp"]["headers"] = {
        "Authorization": f"Bearer {access_token}"
    }
    MCP_JSON_PATH.write_text(json.dumps(settings, indent=2) + "\n")
    print(f"Updated {MCP_JSON_PATH}")


def _try_refresh(refresh_tok: str) -> dict | None:
    """Attempt token refresh via proxy. Returns token response or None."""
    resp = requests.post(
        f"{PROXY_BASE_URL}/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "grant_type": "refresh_token",
            "refresh_token": refresh_tok,
        },
        timeout=30,
    )
    if resp.ok:
        return resp.json()
    print(f"Refresh failed ({resp.status_code}): {resp.text}")
    return None


def _register_client() -> tuple[str, str]:
    """Register a new OAuth client via DCR."""
    resp = requests.post(
        f"{PROXY_BASE_URL}/register",
        json={
            "client_name": "mcp-token-refresh-script",
            "redirect_uris": [LOCAL_REDIRECT_URI],
            "grant_types": ["authorization_code"],
            "response_types": ["code"],
            "token_endpoint_auth_method": "client_secret_post",
        },
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    return data["client_id"], data["client_secret"]


def _full_auth_flow() -> dict:
    """Run full browser OAuth flow. Returns token response dict."""
    cached = _load_cached_tokens()
    client_id = cached.get("client_id")
    client_secret = cached.get("client_secret")

    if not client_id or not client_secret:
        print("Registering new OAuth client...")
        client_id, client_secret = _register_client()
        cached["client_id"] = client_id
        cached["client_secret"] = client_secret
        _save_cached_tokens(cached)

    state = secrets.token_urlsafe(32)
    auth_params = urlencode({
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": LOCAL_REDIRECT_URI,
        "scope": "openid email",
        "state": state,
    })
    auth_url = f"{PROXY_BASE_URL}/authorize?{auth_params}"

    captured = {}

    class CallbackHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            parsed = urlparse(self.path)
            params = parse_qs(parsed.query)
            captured["code"] = params.get("code", [None])[0]
            captured["state"] = params.get("state", [None])[0]
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(b"<h1>Auth complete! You can close this tab.</h1>")

        def log_message(self, _format, *_args):
            pass

    server = HTTPServer(("localhost", LOCAL_PORT), CallbackHandler)
    print(f"Opening browser for authentication...")
    webbrowser.open(auth_url)

    print(f"Waiting for callback on localhost:{LOCAL_PORT} ...")
    server.handle_request()
    server.server_close()

    if not captured.get("code"):
        raise RuntimeError("No authorization code received")
    if captured.get("state") != state:
        raise RuntimeError(f"State mismatch: expected {state}, got {captured.get('state')}")

    print("Exchanging code for tokens...")
    resp = requests.post(
        f"{PROXY_BASE_URL}/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "grant_type": "authorization_code",
            "code": captured["code"],
            "redirect_uri": LOCAL_REDIRECT_URI,
            "client_id": client_id,
            "client_secret": client_secret,
        },
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def main() -> None:
    cached = _load_cached_tokens()
    refresh_tok = cached.get("refresh_token")

    token_data = None
    if refresh_tok:
        print("Attempting token refresh...")
        token_data = _try_refresh(refresh_tok)

    if not token_data:
        print("Full auth flow required.")
        token_data = _full_auth_flow()

    if "refresh_token" in token_data:
        cached = _load_cached_tokens()
        cached["refresh_token"] = token_data["refresh_token"]
        _save_cached_tokens(cached)
        print("Saved new refresh token to cache.")

    access_token = token_data["access_token"]
    _update_mcp_json(access_token)
    print("Token refreshed successfully. Restart Claude Code to pick up the new token.")


if __name__ == "__main__":
    main()
