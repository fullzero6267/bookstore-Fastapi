"""
FastAPI Depends 모음
- 요청마다 DB 세션을 하나씩 생성/종료
"""

from typing import Generator
from sqlalchemy.orm import Session
from app.db.session import SessionLocal

def get_db() -> Generator[Session, None, None]:

    # 요청 시작 시 DB 세션 생성 요청 끝나면 자동 close

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()