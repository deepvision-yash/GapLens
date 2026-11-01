"""Small MVP authentication helpers: PBKDF2 passwords and signed expiring cookies."""
import base64
import hashlib
import hmac
import json
import secrets
import time
from fastapi import HTTPException, Request, status
from app.core.config import settings

TOKEN_COOKIE = "gaplens_auth"
TOKEN_TTL_SECONDS = 60 * 60 * 24 * 7


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 310_000)
    return "pbkdf2_sha256$310000$%s$%s" % (
        base64.urlsafe_b64encode(salt).decode().rstrip("="),
        base64.urlsafe_b64encode(digest).decode().rstrip("="),
    )


def verify_password(password: str, encoded: str) -> bool:
    try:
        algorithm, rounds, salt_text, digest_text = encoded.split("$")
        if algorithm != "pbkdf2_sha256":
            return False
        salt = base64.urlsafe_b64decode(salt_text + "=" * (-len(salt_text) % 4))
        expected = base64.urlsafe_b64decode(digest_text + "=" * (-len(digest_text) % 4))
        actual = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, int(rounds))
        return hmac.compare_digest(actual, expected)
    except (ValueError, TypeError):
        return False


def _secret() -> bytes:
    return settings.AUTH_SECRET_KEY.encode("utf-8")


def create_auth_token(user_id: str) -> str:
    payload = base64.urlsafe_b64encode(json.dumps({"sub": user_id, "exp": int(time.time()) + TOKEN_TTL_SECONDS}, separators=(",", ":")).encode()).decode().rstrip("=")
    signature = hmac.new(_secret(), payload.encode(), hashlib.sha256).digest()
    sig = base64.urlsafe_b64encode(signature).decode().rstrip("=")
    return payload + "." + sig


def user_id_from_request(request: Request) -> str:
    token = request.cookies.get(TOKEN_COOKIE)
    if not token:
        auth = request.headers.get("authorization", "")
        token = auth[7:].strip() if auth.lower().startswith("bearer ") else ""
    try:
        payload, signature = token.split(".", 1)
        expected = base64.urlsafe_b64encode(hmac.new(_secret(), payload.encode(), hashlib.sha256).digest()).decode().rstrip("=")
        if not hmac.compare_digest(signature, expected):
            raise ValueError("signature")
        decoded = base64.urlsafe_b64decode(payload + "=" * (-len(payload) % 4))
        data = json.loads(decoded)
        if int(data["exp"]) < time.time() or not data.get("sub"):
            raise ValueError("expired")
        return str(data["sub"])
    except (ValueError, KeyError, TypeError, json.JSONDecodeError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Sign in to continue.")
