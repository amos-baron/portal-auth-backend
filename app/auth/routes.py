from urllib.parse import urlencode
import json
from fastapi import APIRouter, Depends
import requests
from app.settings import settings
from starlette.responses import RedirectResponse
from fastapi.security.utils import get_authorization_scheme_param
import jwt
from starlette.requests import Request
from .schemas import ValidationJson

LOGIN_URL = f"{settings.keycloak_addr}/auth/realms/{settings.realm}/protocol/openid-connect/auth"
TOKEN_URL = f"{settings.keycloak_addr}/auth/realms/{settings.realm}/protocol/openid-connect/token"
USER_URL = f"{settings.keycloak_addr}/auth/realms/{settings.realm}/protocol/openid-connect/userinfo"
INSPECT_URL = f"{settings.keycloak_addr}/auth/realms/{settings.realm}/protocol/openid-connect/token/introspect"

router = APIRouter()


@router.get("/login")
def get_login_url() -> RedirectResponse:
    params = {
        "client_id": settings.backend_client_id,
        "response_type": "code"
    }
    response = RedirectResponse(f"{LOGIN_URL}?{urlencode(params)}")
    return response


@router.get("/authorize")
async def verify_authorization(code: str) -> RedirectResponse:
    async def get_token():
        payload = (
            f"grant_type=authorization_code&code={code}"
            f"&redirect_uri=http://{settings.app_url}&client_id={settings.backend_client_id}&client_secret={settings.backend_client_secret}"
        )
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        token_response = requests.request(
            "POST", TOKEN_URL, data=payload, headers=headers
        )
        token_body = json.loads(token_response.content)

        keycloak_token = token_body["access_token"]

        return keycloak_token

    token = await get_token()
    response = RedirectResponse(url="/")
    response.set_cookie("Authorization", value=f"Bearer {token}")
    return response


@router.get("/inspect")
async def inspect(request: Request) -> ValidationJson:
    authorization: str = request.cookies.get("Authorization")
    scheme, user_token = get_authorization_scheme_param(authorization)
    payload = (
        f"token={user_token}"
        f"&client_id={settings.backend_client_id}&client_secret={settings.backend_client_secret}"
    )
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    async def inspect_token():
        inspection_response = requests.request(
            "POST", INSPECT_URL, data=payload, headers=headers
        )
        return inspection_response

    token_inspection_response = await inspect_token()
    token_inspection_json = json.loads(token_inspection_response.content)
    return {"validated": token_inspection_json['active']}


@router.get("/info")
async def get_info(request: Request):
    authorization: str = request.cookies.get("Authorization")
    scheme, user_token = get_authorization_scheme_param(authorization)
    decoded = jwt.decode(user_token, options={"verify_signature": False})
    return decoded