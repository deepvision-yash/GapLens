from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import structlog

from app.core.config import settings
from app.core.database import init_db
from app.api.research import router as research_router
from app.api.auth import router as auth_router
from app.services.external import tavily_service, jina_service, llm_service

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer(),
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    if settings.ENVIRONMENT.lower() not in {"development", "dev", "local"} and settings.AUTH_SECRET_KEY == "local-development-key-change-before-deploying":
        raise RuntimeError("Set a unique AUTH_SECRET_KEY before running GapLens outside development.")
    # Startup
    logger.info("Starting GapLens API", version=settings.APP_VERSION)
    await init_db()
    logger.info("Database initialized")
    
    yield
    
    # Shutdown
    logger.info("Shutting down GapLens API")
    await tavily_service.close()
    await jina_service.close()
    await llm_service.close()


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="GapLens - AI Research Intelligence & Information Gap Analysis Engine",
    lifespan=lifespan,
    debug=settings.DEBUG,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(research_router)
app.include_router(auth_router)


@app.get("/")
async def root():
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/landing.html")


@app.get("/login", include_in_schema=False)
async def login_page():
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/login.html")


@app.get("/health")
async def health_check():
    if settings.LLM_PROVIDER.lower() == "groq":
        llm_ready = bool(settings.GROQ_API_KEY)
    else:
        llm_ready = bool(settings.GEMINI_API_KEY or settings.GROQ_API_KEY)
    search_ready = bool(settings.JINA_API_KEY) if settings.SEARCH_PROVIDER.lower() == "jina" else bool(settings.TAVILY_API_KEY)
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "providers": {
            "llm_provider": settings.LLM_PROVIDER,
            "llm_ready": llm_ready,
            "search_provider": settings.SEARCH_PROVIDER,
            "search_ready": search_ready,
            "reader_ready": True,
        },
    }


@app.get("/research/new", include_in_schema=False)
async def research_home_page():
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/research_home.html")


@app.get("/research/{session_id}/{screen}", include_in_schema=False)
async def research_session_page(session_id: str, screen: str):
    from fastapi.responses import RedirectResponse
    pages = {
        "scope": "research_scope.html",
        "progress": "research_in_progress.html",
        "intelligence": "research_intelligence.html",
        "evidence": "evidence_explorer.html",
        "verification": "verification_workspace.html",
    }
    page = pages.get(screen)
    if not page:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Research screen not found.")
    return RedirectResponse(url=f"/{page}?session_id={session_id}")


# Serve the provided Stitch HTML pages directly; API routes above retain priority.
HTML_FRONTEND_DIR = Path(__file__).resolve().parents[2] / "frontend" / "html"


@app.get("/app.js", include_in_schema=False)
async def frontend_application_script():
    """Serve current frontend logic without stale browser caching in the MVP."""
    return FileResponse(
        HTML_FRONTEND_DIR / "app.js",
        media_type="application/javascript",
        headers={"Cache-Control": "no-store, no-cache, must-revalidate"},
    )


app.mount("/", StaticFiles(directory=HTML_FRONTEND_DIR, html=True), name="html-frontend")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
    )
