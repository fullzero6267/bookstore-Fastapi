"""
FastAPI 애플리케이션 엔트리 포인트
"""

# src/app/main.py
from fastapi import FastAPI

# 각 기능별 API 라우터들을 import
# 기능 단위(Auth, Users, Books)로 파일을 분리
from app.api.routes import Auth, Users, Books, Carts, Orders, Favorites, Reviews

# FastAPI 애플리케이션 객체 생성
# title은 Swagger(/docs)에 표시될 API 이름
app = FastAPI(title="Bookstore API Chan")

#api
app.include_router(Auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(Users.router, prefix="/api/users", tags=["Users"])
app.include_router(Books.router, prefix="/api", tags=["Books"])      # /api/books, /api/public/books
app.include_router(Carts.router, prefix="/api/carts", tags=["Carts"])
app.include_router(Orders.router, prefix="/api/orders", tags=["Orders"])
app.include_router(Favorites.router, prefix="/api/favorites", tags=["Favorites"])
app.include_router(Reviews.router, prefix="/api", tags=["Reviews"])  # /api/books/{bookId}/reviews, /api/reviews/...