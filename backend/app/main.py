import logging
import time
from contextlib import asynccontextmanager

from pathlib import Path

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from jose import jwt, JWTError
from starlette.middleware.base import BaseHTTPMiddleware

from app.config import settings
from app.api.v1.router import api_router

access_logger = logging.getLogger("ezlove.access")


@asynccontextmanager
async def lifespan(app: FastAPI):
    from app.tasks.alert_checker import start_scheduler
    start_scheduler()
    yield
    from app.tasks.alert_checker import shutdown_scheduler
    shutdown_scheduler()


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        return response


class AccessLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()
        response: Response = await call_next(request)
        duration_ms = (time.perf_counter() - start) * 1000

        user_id = self._extract_user_id(request)
        access_logger.info(
            "%s %s %d uid=%s %.1fms",
            request.method, request.url.path, response.status_code,
            user_id or "-", duration_ms,
        )
        return response

    @staticmethod
    def _extract_user_id(request: Request) -> str | None:
        auth = request.headers.get("authorization")
        if not auth or not auth.lower().startswith("bearer "):
            return None
        try:
            payload = jwt.decode(auth[7:], settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM], options={"verify_exp": False})
            return payload.get("sub")
        except JWTError:
            return None


app = FastAPI(
    title=settings.APP_NAME,
    lifespan=lifespan,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(AccessLogMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.DEBUG else settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"] if settings.DEBUG else ["Authorization", "Content-Type"],
)

app.include_router(api_router, prefix="/api/v1")

static_dir = Path(__file__).resolve().parents[1] / "static"
static_dir.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


@app.get("/health")
async def health_check():
    return {"status": "ok"}
