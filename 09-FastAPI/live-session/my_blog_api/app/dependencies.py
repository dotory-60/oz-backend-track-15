# app/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.crud.user import get_user_by_username
from app.db.session import AsyncSessionLocal
from app.utils.security import verify_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


# ------------------------ DML 감지 로직 ------------------------
@event.listens_for(Session, "do_orm_execute")
def _flag_write_on_orm_execute(orm_execute_state):
    """
    ORM 구문(Session.execute(...)) 중 DML만 플래그 세팅.
    - UPDATE/DELETE: True
    - SELECT: 제외
    - INSERT: 보통 ORM flush 경로에서 처리 → after_flush가 커버
    """
    if getattr(orm_execute_state, "is_update", False) or getattr(
        orm_execute_state, "is_delete", False
    ):
        orm_execute_state.session.info["__had_write__"] = True


@event.listens_for(Session, "after_flush")
def _flag_write_after_flush(session: Session, flush_context) -> None:
    # ORM add/dirty/delete → flush에서 실제 DML 발생 시만 True
    if session.new or session.dirty or session.deleted:
        session.info["__had_write__"] = True


# ------------------------ FastAPI DI ------------------------
# ✅ SELECT-only: commit/rollback 호출 안 함
# ✅ DML 발생: 종료 시 commit, 예외 시 rollback
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            # 중요: 먼저 세션을 주입해서( yield ) 라우터/서비스가 사용하게 해야 함
            yield session

            # 정상 종료 시, DML이 있었을 때만 커밋
            if session.info.pop("__had_write__", False):
                print("commit")
                await session.commit()
            # SELECT-only: 아무 것도 호출하지 않음 (커넥션 반납 시 엔진이 ROLLBACK로 스냅샷 정리)
        except Exception:
            # 예외 시, DML이 있었던 경우에만 롤백
            if session.info.get("__had_write__", False):
                print("rollback")
                await session.rollback()
            raise
        # async with 블록 종료 시 세션/커넥션은 자동 close


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
):
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = verify_access_token(token)  # 내부에서 키/알고리즘/iss/aud/exp 모두 처리
        username = payload.get("sub")
        if not username:
            raise credentials_error
    except Exception as e:
        print(e)
        raise credentials_error

    user = await get_user_by_username(db, username)
    if not user:
        raise credentials_error
    return user
