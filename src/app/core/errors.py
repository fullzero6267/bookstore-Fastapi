from fastapi import HTTPException, status

#에러 미리 세팅
def raise_not_found(code: str = "RESOURCE_NOT_FOUND"):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=code)

def raise_conflict(code: str = "DUPLICATE_RESOURCE"):
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=code)

def raise_unauthorized(code: str = "UNAUTHORIZED"):
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=code)

def raise_forbidden(code: str = "FORBIDDEN"):
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=code)