
from app.api.routes import html
from fastapi.staticfiles import StaticFiles
import sentry_sdk
from fastapi import FastAPI
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware

from app.api.main import api_router
from app.core.config import settings


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


if settings.SENTRY_DSN and settings.ENVIRONMENT != "local":
    sentry_sdk.init(dsn=str(settings.SENTRY_DSN), enable_tracing=True)



app = FastAPI(
    title="Sigmatch",
    version="1.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
    description="Документация API для управления данными и процессами проекта по хакатону MIRE/A\\TOM"
)

app.mount("/static", StaticFiles(directory="/app/app/templates"), name="static")
# Set all CORS enabled origins
#if settings.all_cors_origins:
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["POST", "GET", "PUT", "DELETE", "OPTIONS", "PATCH"],
	allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(html.router,  tags=["HTML Content"])
