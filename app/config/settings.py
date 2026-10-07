from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    database_url: str = (
        "postgresql+psycopg2://postgres:postgres@localhost:5432/mcp_gateway"
    )

    jwt_secret_key: str = (
        "enterprise-mcp-gateway-secret-key-2026-strong"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()