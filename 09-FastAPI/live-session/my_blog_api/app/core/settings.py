# app/core/settings.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

class SecuritySettings(BaseSettings):
    # JWT
    jwt_algorithm: str = "HS256"
    access_token_exp_minutes: int = 60

    # HS* (대칭키)
    secret_key: SecretStr | None = None  # ex) 32바이트 이상 랜덤 문자열

    # RS* (비대칭키, PEM)
    jwt_private_key: SecretStr | None = None  # -----BEGIN PRIVATE KEY-----
    jwt_public_key: SecretStr | None = None   # -----BEGIN PUBLIC KEY-----

    # 표준 클레임(선택)
    jwt_issuer: str | None = None
    jwt_audience: str | None = None

    # Argon2 파라미터
    argon2_time_cost: int = 3
    argon2_memory_cost: int = 32768  # KB
    argon2_parallelism: int = 1

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        env_prefix="",  # 원하는 경우 "JWT_" 등 prefix를 둘 수 있음
    )

security_settings = SecuritySettings()
