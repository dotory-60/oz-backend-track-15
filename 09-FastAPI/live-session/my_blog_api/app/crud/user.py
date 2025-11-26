# app/crud/user.py
from typing import Optional, Any, Dict
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import UserCreate
from app.utils.security import get_password_hash_async  # async 래퍼 사용


class UserAlreadyExists(Exception):
    """중복 사용자 예외: 기본 409"""
    status_code: int = 409
    code: str = "user_already_exists"

    def __init__(
        self,
        message: str = "user already exists",
        *,
        field: Optional[str] = None,
        value: Optional[str] = None,
    ) -> None:
        super().__init__(message)
        self.field = field
        self.value = value

    def to_dict(self) -> Dict[str, Any]:
        return {
            "error": self.code,
            "message": str(self),
            "field": self.field,
            "value": self.value,
        }


class UserNotFound(Exception):
    """사용자 미존재 예외: 기본 404"""
    status_code: int = 404
    code: str = "user_not_found"

    def __init__(
        self,
        message: str = "user not found",
        *,
        user_id: Optional[int] = None,
        username: Optional[str] = None,
        email: Optional[str] = None,
    ) -> None:
        super().__init__(message)
        self.user_id = user_id
        self.username = username
        self.email = email

    def to_dict(self) -> Dict[str, Any]:
        return {
            "error": self.code,
            "message": str(self),
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
        }


# ✅ PK 조회는 .get() 사용(아이덴티티 맵/1차 캐시 활용)
async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
    return await db.get(User, user_id)

async def get_user_by_username(db: AsyncSession, username: str) -> User | None:
    res = await db.execute(select(User).where(User.username == username))
    return res.scalar_one_or_none()

async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    res = await db.execute(select(User).where(User.email == email))
    return res.scalar_one_or_none()


async def create_user(db: AsyncSession, data: UserCreate) -> User:
    # 1) CPU-bound 해시를 스레드풀로 오프로딩
    password_hash = await get_password_hash_async(data.password)

    user = User(username=data.username, email=data.email, password_hash=password_hash)
    db.add(user)

    # 2) 조기 제약 검증: flush 시 INSERT 수행 → Unique 위반 즉시 발생
    try:
        await db.flush()
    except IntegrityError as e:
        # ❌ 여기서 rollback하지 않음: DI(get_session)가 일괄 처리
        # (선택) constraint 이름 파싱해 메시지 세분화
        #   PG 예: cname = getattr(getattr(e, "orig", None), "diag", None)
        #          and getattr(cname, "constraint_name", None)
        raise UserAlreadyExists("username or email already exists") from e

    # 3) 서버 default(now) 등 동기화
    await db.refresh(user)
    # ❌ commit은 DI가 최종 처리
    return user
