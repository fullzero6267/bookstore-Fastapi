"""
User 관련 API 라우터
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.security import get_password_hash
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse

# /users 로 시작하는 API
router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post(
    "",
    response_model=UserResponse,
    status_code=201
)
def register_user(
    payload: UserCreate,
    db: Session = Depends(get_db)
):
    """
    회원가입 API
    - 이메일 중복 체크
    - 비밀번호 해시 후 저장
    """

    # 1. 이메일 중복 확인
    exists = db.query(User).filter(
        User.email == payload.email
    ).first()

    if exists:
        raise HTTPException(
            status_code=409,
            detail="DUPLICATE_RESOURCE"
        )

    # 2. User 객체 생성
    user = User(
        email=payload.email,
        password_hash=get_password_hash(payload.password),
        name=payload.name,
        role="ROLE_USER",
        is_active=True,
    )

    # 3. DB 저장
    db.add(user)
    db.commit()
    db.refresh(user)

    return user