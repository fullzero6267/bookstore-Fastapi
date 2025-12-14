# src/app/core/jwt.py
from datetime import datetime, timedelta, timezone
from jose import jwt
from app.core.config import get_settings
import uuid

settings = get_settings()

def _now_utc() -> datetime:
    # UTC 기준 시간 (JWT 표준)
    return datetime.now(timezone.utc)

def create_access_token(subject: str, role: str) -> str:
    """
    subject: user_id를 문자열로 넣음
    role: ROLE_USER / ROLE_ADMIN
    """
    expire = _now_utc() + timedelta(minutes=settings.access_token_expire_minutes)
    payload = {
        "type": "access",
        "sub": subject,
        "role": role,
        "exp": expire,
        "iat": _now_utc(),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)

def create_refresh_token(subject: str) -> tuple[str, str, datetime]:
    """
    refresh token은 DB에 'jti'를 저장해서 로그아웃/폐기 가능하게 만든다.
    return: (token, jti, expires_at)
    """
    expire = _now_utc() + timedelta(days=settings.refresh_token_expire_days)
    jti = str(uuid.uuid4())
    payload = {
        "type": "refresh",
        "sub": subject,
        "jti": jti,
        "exp": expire,
        "iat": _now_utc(),
    }
    token = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)
    return token, jti, expire