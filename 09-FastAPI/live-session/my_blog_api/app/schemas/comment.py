from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class CommentBase(BaseModel):
    content: str = Field(min_length=1, max_length=10_000)

class CommentCreate(CommentBase):
    pass

class CommentRead(CommentBase):
    id: int
    owner_id: int
    post_id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
