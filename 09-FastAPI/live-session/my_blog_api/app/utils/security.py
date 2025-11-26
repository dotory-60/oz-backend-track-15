# app/utils/security.py
from datetime import datetime, timedelta, timezone
from typing import Any, Final, Mapping, Tuple

from jose import jwt
from passlib.context import CryptContext
from starlette.concurrency import run_in_threadpool

from app.core.settings import security_settings as S  # ✅ 중앙 설정에서 주입

# ==========================
# Password hashing (Argon2)
# ==========================
_PWD_CTX: Final = CryptContext(
    schemes=["argon2"],
    deprecated="auto",
    argon2__time_cost=S.argon2_time_cost,
    argon2__memory_cost=S.argon2_memory_cost,   # KB
    argon2__parallelism=S.argon2_parallelism,
)

def get_password_hash(plain: str) -> str:
    return _PWD_CTX.hash(plain)

def verify_password(plain: str, hashed: str) -> bool:
    return _PWD_CTX.verify(plain, hashed)

def needs_rehash(hashed: str) -> bool:
    return _PWD_CTX.needs_update(hashed)

# async (CPU-bound offload)
async def get_password_hash_async(plain: str) -> str:
    return await run_in_threadpool(_PWD_CTX.hash, plain)

async def verify_password_async(plain: str, hashed: str) -> bool:
    return await run_in_threadpool(_PWD_CTX.verify, plain, hashed)

# ==========================
# JWT helpers
# ==========================
def _now_utc() -> datetime:
    return datetime.now(timezone.utc)

def _pick_signing_key_and_headers() -> Tuple[str, dict[str, Any]]:
    """
    서명 키와 JWT 헤더 결정:
    - HS*: secret_key
    - RS*: jwt_private_key
    """
    headers: dict[str, Any] = {"typ": "JWT"}
    alg = S.jwt_algorithm.upper()

    if alg.startswith("HS"):
        key = S.secret_key.get_secret_value() if S.secret_key else None
        if not key:
            raise RuntimeError("SECRET_KEY is required for HS* algorithms")
        return key, headers

    if alg.startswith("RS"):
        key = S.jwt_private_key.get_secret_value() if S.jwt_private_key else None
        if not key:
            raise RuntimeError("JWT_PRIVATE_KEY is required for RS* algorithms")
        return key, headers

    raise RuntimeError(f"Unsupported JWT algorithm: {S.jwt_algorithm}")

def _pick_verify_key() -> str:
    """
    검증 키 결정:
    - HS*: secret_key
    - RS*: jwt_public_key
    """
    alg = S.jwt_algorithm.upper()

    if alg.startswith("HS"):
        key = S.secret_key.get_secret_value() if S.secret_key else None
        if not key:
            raise RuntimeError("SECRET_KEY is required for HS* algorithms")
        return key

    if alg.startswith("RS"):
        key = S.jwt_public_key.get_secret_value() if S.jwt_public_key else None
        if not key:
            raise RuntimeError("JWT_PUBLIC_KEY is required for RS* algorithms")
        return key

    raise RuntimeError(f"Unsupported JWT algorithm: {S.jwt_algorithm}")

# ---------- 발급 ----------
def create_access_token(
    subject: str,
    expires_delta: timedelta | None = None,
    *,
    scopes: list[str] | None = None,
    extra: Mapping[str, Any] | None = None,
    kid: str | None = None,  # 키 로테이션용 선택 헤더
) -> str:
    if not subject or not subject.strip():
        raise ValueError("subject is required")

    now = _now_utc()
    exp_at = now + (expires_delta or timedelta(minutes=S.access_token_exp_minutes))

    payload: dict[str, Any] = {
        "sub": subject,
        "iat": int(now.timestamp()),
        "exp": int(exp_at.timestamp()),
    }
    if S.jwt_issuer:
        payload["iss"] = S.jwt_issuer
    if S.jwt_audience:
        payload["aud"] = S.jwt_audience
    if scopes:
        payload["scope"] = list(scopes)  # None일 때만 미포함

    if extra:
        payload.update(extra)

    key, headers = _pick_signing_key_and_headers()
    if kid:
        headers = {**headers, "kid": kid}

    return jwt.encode(payload, key, algorithm=S.jwt_algorithm, headers=headers)

# ---------- 검증 ----------
def verify_access_token(
    token: str,
) -> dict[str, Any]:
    key = _pick_verify_key()
    alg = S.jwt_algorithm

    options = {
        "verify_signature": True,
        "verify_exp": True,
        "verify_aud": bool(S.jwt_audience),
        "verify_iss": bool(S.jwt_issuer),
        "require_exp": True,
        "require_iat": True,
        # 정책상 강제하려면:
        # "require_sub": True,
    }

    return jwt.decode(
        token,
        key,
        algorithms=[alg],
        audience=S.jwt_audience if S.jwt_audience else None,
        issuer=S.jwt_issuer if S.jwt_issuer else None,
        options=options
    )
