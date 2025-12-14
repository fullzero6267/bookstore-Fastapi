import uuid
from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.auth import LoginRequest, TokenResponse
from app.core.security import verify_password, create_access_token, create_refresh_token
from app.models.user import User
from app.models.refresh_token import RefreshToken
from app.core.config import get_settings
from jose import jwt, JWTError

router = APIRouter(prefix="/auth", tags=["auth"])
settings = get_settings()

@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access = create_access_token(str(user.id))

    jti = str(uuid.uuid4())
    refresh = create_refresh_token(str(user.id), jti)

    expires_at = datetime.now(timezone.utc) + timedelta(days=settings.jwt_refresh_token_expire_days)
    db.add(RefreshToken(user_id=user.id, jti=jti, expires_at=expires_at, is_revoked=False))
    db.commit()

    return TokenResponse(access_token=access, refresh_token=refresh)

@router.post("/refresh", response_model=TokenResponse)
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(refresh_token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Not a refresh token")
        user_id = payload.get("sub")
        jti = payload.get("jti")
        if not user_id or not jti:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    token_row = db.query(RefreshToken).filter(RefreshToken.jti == jti).first()
    if not token_row or token_row.is_revoked:
        raise HTTPException(status_code=401, detail="Refresh token revoked or not found")

    # 만료 체크
    if token_row.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
        raise HTTPException(status_code=401, detail="Refresh token expired")

    access = create_access_token(str(user_id))
    # refresh는 그대로 유지하거나(단순), rotate하려면 여기서 새로 발급+기존 revoke 처리

    return TokenResponse(access_token=access, refresh_token=refresh_token)