from pydantic_settings import BaseSettings
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base


# DB 접속 URL 관리
class Settings(BaseSettings):
    db_host: str = "localhost"
    db_port: int = 5432
    db_user: str = "myuser"
    db_password: str = "mypass"
    db_name: str = "myblog"

    @property
    def async_db_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    class Config:
        env_file = ".env"
        extra = "ignore"  # 필요 없는 속성은 무시해, 예를 들어 .env 파일에 필요없는 속성이 들어있을 경우 무시한다는 의미


settings = Settings()

# DB 연결 담당, postgresql에 적절하게 설정
engine = create_async_engine(
    settings.async_db_url,
    echo=True,
    pool_pre_ping=True,
    pool_size=1,  # 커넥션 풀 크기
    max_overflow=1,  # 커넥션 풀 최대 초과 크기
    pool_timeout=30,  # 커넥션 풀 타임아웃 시간 (30초)
)

# 실제 DB 세션 만들어주는 공장
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

# 모든 모델의 부모 클래스
Base = declarative_base()
