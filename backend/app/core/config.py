from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AliasChoices, Field
from typing import Optional, List
import json


class Settings(BaseSettings):
    # App
    APP_NAME: str = "GapLens API"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    LLM_PROVIDER: str = "gemini"
    GEMINI_MODEL: str = "gemini-3.8-flash"
    GROQ_MODEL: str = "openai/gpt-oss-20b"
    SEARCH_PROVIDER: str = "jina"
    JINA_EMBEDDING_MODEL: str = "jina-embeddings-v3"
    AUTH_SECRET_KEY: str = "local-development-key-change-before-deploying"
    
    # CORS (stored as JSON string in .env)
    CORS_ORIGINS_JSON: str = Field(
        default='["http://localhost:3000", "http://localhost:3001"]',
        validation_alias=AliasChoices("CORS_ORIGINS_JSON", "CORS_ORIGINS"),
    )
    
    @property
    def CORS_ORIGINS(self) -> List[str]:
        try:
            return json.loads(self.CORS_ORIGINS_JSON)
        except json.JSONDecodeError:
            return [origin.strip() for origin in self.CORS_ORIGINS_JSON.split(",") if origin.strip()]
    
    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./gaplens.db"
    
    # Tavily API
    TAVILY_API_KEY: Optional[str] = Field(default=None)
    
    # Jina AI
    JINA_API_KEY: Optional[str] = Field(default=None)
    
    # Google Gemini
    GEMINI_API_KEY: Optional[str] = Field(default=None)
    
    # Groq
    GROQ_API_KEY: Optional[str] = Field(default=None)
    
    # Pipeline settings
    MAX_SOURCES_PER_SESSION: int = 10
    MAX_DIMENSIONS: int = 6
    SEARCH_DEPTH: str = "advanced"  # basic, advanced
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 100
    EMBEDDING_DIM: int = 1024
    
    # SSE
    SSE_RETRY_MS: int = 3000
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()
