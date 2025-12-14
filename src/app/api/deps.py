from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.core.security import decode_access_token
from app.models.user import User
from app.db.session import get_db
from app.core.security import decode_token
from app.core.errors import raise_unauthorized

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
) -> User:
    #현재 로그인한 유저 가져오기 authorization: Bearer 필요
    payload = decode_token(token)

    #access 토큰 확인
    if payload.get("type") != "access":
        raise_unauthorized("INVALID_TOKEN_TYPE")

    user_id = payload.get("sub")
    if not user_id:
        raise_unauthorized("INVALID_TOKEN")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise_unauthorized("USER_NOT_FOUND")
    return user