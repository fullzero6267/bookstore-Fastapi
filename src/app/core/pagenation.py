from sqlalchemy.orm import Query

def paginate(query: Query, page: int = 0, size: int = 20):

    #공통 페이지네이션 페이지 0 부터 시작하고 size가 20임
    if page < 0:
        page = 0
    if size <= 0:
        size = 20
    if size > 100:
        size = 100

    total = query.count()
    items = query.offset((page * size)).limit(size).all()
    total_pages = (total + size -1) // size

    return {
        "content": itmes,
        "page": page,
        "size": size,
        "totalElements": total,
        "totalPages": total_pages,
    }