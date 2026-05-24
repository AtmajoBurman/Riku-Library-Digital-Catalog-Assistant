import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import model_validator

# Get the absolute path to the RESTAPI_project root directory
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENV_FILE_PATH = os.path.join(ROOT_DIR, ".env")

class Settings(BaseSettings):
    POSTGRES_URL: Optional[str] = None
    DATABASE_URL: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH,
        extra="ignore"
    )

    @model_validator(mode="after")
    def check_database_url(self) -> "Settings":
        if not self.POSTGRES_URL and not self.DATABASE_URL:
            raise ValueError("Either POSTGRES_URL or DATABASE_URL must be provided in the .env file")
        return self

    def _clean_and_encode_db_url(self, url: str) -> str:
        import urllib.parse
        if not url or "://" not in url:
            return url
        scheme, rest = url.split("://", 1)
        if "@" not in rest:
            return url
        creds, host_db = rest.rsplit("@", 1)
        if ":" in creds:
            username, password = creds.split(":", 1)
            username = urllib.parse.quote_plus(urllib.parse.unquote(username))
            password = urllib.parse.quote_plus(urllib.parse.unquote(password))
            creds = f"{username}:{password}"
        else:
            creds = urllib.parse.quote_plus(urllib.parse.unquote(creds))
        return f"{scheme}://{creds}@{host_db}"

    @property
    def raw_database_url(self) -> str:
        url = self.DATABASE_URL or self.POSTGRES_URL
        if not url:
            raise ValueError("Either POSTGRES_URL or DATABASE_URL must be provided in the .env file")
        return self._clean_and_encode_db_url(url)

    @property
    def async_database_url(self) -> str:
        url = self.raw_database_url
        if "+asyncpg" in url or "+aiosqlite" in url or "+aiomysql" in url or "+asyncmy" in url:
            return url
        
        if url.startswith("postgresql://"):
            return url.replace("postgresql://", "postgresql+asyncpg://", 1)
        elif url.startswith("postgres://"):
            return url.replace("postgres://", "postgresql+asyncpg://", 1)
        elif url.startswith("sqlite://"):
            return url.replace("sqlite://", "sqlite+aiosqlite://", 1)
        elif url.startswith("mysql://"):
            return url.replace("mysql://", "mysql+aiomysql://", 1)
        return url

    @property
    def sync_database_url(self) -> str:
        url = self.raw_database_url
        if url.startswith("postgresql+asyncpg://"):
            url = url.replace("postgresql+asyncpg://", "postgresql://", 1)
        elif url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql://", 1)
        elif url.startswith("sqlite+aiosqlite://"):
            url = url.replace("sqlite+aiosqlite://", "sqlite://", 1)
        elif url.startswith("mysql+aiomysql://"):
            url = url.replace("mysql+aiomysql://", "mysql://", 1)
        elif url.startswith("mysql+asyncmy://"):
            url = url.replace("mysql+asyncmy://", "mysql://", 1)
        
        if "ssl=require" in url:
            url = url.replace("ssl=require", "sslmode=require")
        return url

settings = Settings()

print(settings.model_dump())