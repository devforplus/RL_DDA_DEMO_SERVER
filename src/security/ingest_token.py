import base64
import hmac
import json
from datetime import datetime, timedelta, timezone
from hashlib import sha256
from typing import Any


def sign_ingest_token(secret: str, session_id: str, ttl_seconds: int = 3600) -> str:
    payload = {
        "sid": session_id,
        "exp": int((datetime.now(tz=timezone.utc) + timedelta(seconds=ttl_seconds)).timestamp()),
    }
    body = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    sig = hmac.new(secret.encode("utf-8"), body, sha256).digest()
    token = base64.urlsafe_b64encode(body + b"." + sig).decode("ascii").rstrip("=")
    return token


def verify_ingest_token(secret: str, token: str) -> dict[str, Any]:
    padded = token + "=" * (-len(token) % 4)
    data = base64.urlsafe_b64decode(padded.encode("ascii"))
    body, sig = data.rsplit(b".", 1)
    expected = hmac.new(secret.encode("utf-8"), body, sha256).digest()
    if not hmac.compare_digest(sig, expected):
        raise ValueError("invalid signature")
    payload = json.loads(body.decode("utf-8"))
    if int(payload.get("exp", 0)) < int(datetime.now(tz=timezone.utc).timestamp()):
        raise ValueError("token expired")
    return payload


