from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.comment import Comment
from app.schemas.comment import CommentCreate

async def create_comment(db: AsyncSession, owner_id: int, post_id: int, data: CommentCreate) -> Comment:
    c = Comment(content=data.content, owner_id=owner_id, post_id=post_id)
    db.add(c)
    await db.commit()
    await db.refresh(c)
    return c

async def list_comments_by_post(db: AsyncSession, post_id: int) -> list[Comment]:
    res = await db.execute(select(Comment).where(Comment.post_id == post_id).order_by(Comment.id.asc()))
    return list(res.scalars().all())

async def delete_comment(db: AsyncSession, comment_id: int, owner_id: int) -> bool:
    # 간단 검증: 소유자 일치 시 삭제 (강의용)
    res = await db.execute(select(Comment).where(Comment.id == comment_id))
    comment = res.scalar_one_or_none()
    if not comment or comment.owner_id != owner_id:
        return False
    await db.delete(comment)
    await db.commit()
    return True
