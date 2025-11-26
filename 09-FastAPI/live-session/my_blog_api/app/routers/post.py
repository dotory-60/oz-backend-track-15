from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db, get_current_user
from app.models.user import User as UserModel
from app.schemas.post import PostCreate, PostRead, PostUpdate
from app.schemas.comment import CommentCreate, CommentRead
from app.crud.post import create_post, get_post, list_posts, update_post, delete_post
from app.crud.comment import create_comment, list_comments_by_post, delete_comment

router = APIRouter(prefix="/posts", tags=["posts"])

# 게시글 생성 (인증 필요)
@router.post("/", response_model=PostRead, status_code=status.HTTP_201_CREATED)
async def create_post_api(
    payload: PostCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    post = await create_post(db, owner_id=current_user.id, data=payload)
    return post

# 게시글 단건 조회 (비인증 허용)
@router.get("/{post_id}", response_model=PostRead)
async def get_post_api(post_id: int, db: AsyncSession = Depends(get_db)):
    post = await get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="post not found")
    return post

# 게시글 목록 (비인증 허용)
@router.get("/", response_model=list[PostRead])
async def list_posts_api(
    db: AsyncSession = Depends(get_db),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    posts = await list_posts(db, limit=limit, offset=offset)
    return list(posts)

# 게시글 수정 (인가: 소유자만)
@router.put("/{post_id}", response_model=PostRead)
async def update_post_api(
    post_id: int,
    payload: PostUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    post = await get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="post not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="forbidden: not the owner")
    updated = await update_post(db, post_id, payload)
    return updated

# 게시글 삭제 (인가: 소유자만)
@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post_api(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    post = await get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="post not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="forbidden: not the owner")
    ok = await delete_post(db, post_id)
    if not ok:
        raise HTTPException(status_code=400, detail="delete failed")

# ===== 댓글 =====

# 댓글 생성 (인증 필요)
@router.post("/{post_id}/comments", response_model=CommentRead, status_code=status.HTTP_201_CREATED)
async def create_comment_api(
    post_id: int,
    payload: CommentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    post = await get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="post not found")
    comment = await create_comment(db, owner_id=current_user.id, post_id=post_id, data=payload)
    return comment

# 댓글 목록 (비인증 허용)
@router.get("/{post_id}/comments", response_model=list[CommentRead])
async def list_comments_api(post_id: int, db: AsyncSession = Depends(get_db)):
    post = await get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="post not found")
    comments = await list_comments_by_post(db, post_id)
    return comments

# 댓글 삭제 (인가: 본인만)
@router.delete("/{post_id}/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment_api(
    post_id: int,
    comment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    post = await get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="post not found")
    ok = await delete_comment(db, comment_id, owner_id=current_user.id)
    if not ok:
        raise HTTPException(status_code=403, detail="forbidden or not found")
