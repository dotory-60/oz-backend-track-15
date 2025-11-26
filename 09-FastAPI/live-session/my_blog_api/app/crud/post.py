from typing import Sequence
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate

async def create_post(db: AsyncSession, owner_id: int, data: PostCreate) -> Post:
        post = Post(title=data.title, content=data.content, owner_id=owner_id)
        db.add(post)
        await db.commit()
        await db.refresh(post)
        return post

async def get_post(db: AsyncSession, post_id: int) -> Post | None:
        stmt = select(Post).options(selectinload(Post.comments)).where(Post.id == post_id)
        res = await db.execute(stmt)
        return res.scalar_one_or_none()

async def list_posts(db: AsyncSession, limit: int = 20, offset: int = 0) -> Sequence[Post]:
        stmt = (
                select(Post)
                .options(selectinload(Post.comments))
                .order_by(Post.id.desc())
                .limit(limit).offset(offset)
        )
        res = await db.execute(stmt)
        return res.scalars().all()

async def update_post(db: AsyncSession, post_id: int, data: PostUpdate) -> Post | None:
        stmt = (
                update(Post)
                .where(Post.id == post_id)
                .values({k: v for k, v in data.model_dump(exclude_none=True).items()})
                .returning(Post)
        )
        res = await db.execute(stmt)
        post = res.scalar_one_or_none()
        if post:
                await db.commit()
                await db.refresh(post)
        return post

async def delete_post(db: AsyncSession, post_id: int) -> bool:
        res = await db.execute(delete(Post).where(Post.id == post_id))
        await db.commit()
        return res.rowcount > 0
