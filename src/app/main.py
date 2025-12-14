"""
FastAPI 애플리케이션 엔트리 포인트
"""

from fastapi import FastAPI
from app.api.routes.users import router as users_router
from app.api.routes.auth import router as auth_router

app = FastAPI(
    title="Bookstore",
    version="1.0.0"
)

@app.get("/health")
def health():

    # 헬스체크 - 배포 과제 필수
    return {"status": "OK"}

# User API 등록
app.include_router(users_router)
app.include_router(auth_router)