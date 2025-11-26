# app/routers/user.py
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.user import (
    UserAlreadyExists,
    create_user,
    get_user_by_id,
)
from app.dependencies import (
    get_current_user,
    get_db,  # ✅ DI 일원화
)
from app.models.user import User as UserModel
from app.schemas.user import UserCreate, UserRead

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "",  # ✅ trailing slash 제거로 일관성 유지 (선호 스타일)
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    payload: UserCreate,
    response: Response,
    db: AsyncSession = Depends(get_db),
):
    try:
        user = await create_user(db, payload)
        # ✅ 201 Created 모범사례: Location 헤더 설정
        response.headers["Location"] = f"/users/{user.id}"
        return user
    except UserAlreadyExists as e:
        # ✅ 409로 매핑 + 표준화된 에러 바디
        raise HTTPException(status_code=e.status_code, detail=e.to_dict())


@router.get("/{user_id}", response_model=UserRead)
async def read_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),  # 🔐 보호
):
    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return user
