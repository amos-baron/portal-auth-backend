from fastapi import APIRouter, Depends
from typing import Any, Dict
from starlette.requests import Request
from app.auth.routes import validate, get_info
from app.settings import settings
from starlette.responses import RedirectResponse

APP_INSPECT_URL = f"http://{settings.app_url}/auth/inspect"

router = APIRouter()


@router.get("/all")
async def get_user_info(request: Request) -> Dict:
    validation_result = await validate(request)

    if not validation_result["validated"]:
        response = RedirectResponse(url="/auth/login")
        return response

    return await get_info(request)