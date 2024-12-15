from fastapi import APIRouter

from app.api.routes import latex, login, users, utils, math
api_router = APIRouter()
api_router.include_router(login.router, tags=["Авторизация"])
api_router.include_router(users.router, prefix="/users", tags=["Пользователи"])
api_router.include_router(utils.router, prefix="/utils", tags=["Утилиты - ТЕСТЫ"])
api_router.include_router(math.router, prefix="/math", tags=["Математика"])
api_router.include_router(latex.router, prefix="/latex", tags=["LaTeX"])
