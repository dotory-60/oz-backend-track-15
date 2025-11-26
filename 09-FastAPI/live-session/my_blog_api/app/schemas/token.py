from typing import Literal
from pydantic import BaseModel, ConfigDict, Field

class Token(BaseModel):
    access_token: str
    token_type: Literal["bearer"] = "bearer"
    model_config = ConfigDict(extra="forbid") # 알 수 없는 필드 거부

class TokenPayload(BaseModel):
    # JWT 표준/관용 클레임
    sub: str                    # 주체 (일반적으로 username 또는 user_id)
    exp: int | None = None      # 만료 (Unix seconds)
    iat: int | None = None      # 발급 시각
    nbf: int | None = None      # 활성화 시작 시각
    iss: str | None = None      # 발급자
    aud: str | None = None      # 대상자
    scope: list[str] = Field(default_factory=list)
    model_config = ConfigDict(extra="ignore")