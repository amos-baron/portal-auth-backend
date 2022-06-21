from urllib.parse import urlencode
import json
from fastapi import APIRouter, Depends
import requests
from app.settings import settings
from starlette.responses import RedirectResponse
from fastapi.security.utils import get_authorization_scheme_param
import jwt
from starlette.requests import Request
from .schemas import ValidationJson, KeyCloakUser
from .helpers import create_access_token,validate_user_token

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
            f"&redirect_uri=http://{settings.app_url}&client_id={settings.backend_client_id}"
            f"&client_secret={settings.backend_client_secret}"
        )
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        token_response = requests.request(
            "POST", TOKEN_URL, data=payload, headers=headers
        )
        response_body = json.loads(token_response.content)
        keycloak_token = response_body["access_token"]
        decoded_keycloak_token = jwt.decode(keycloak_token, options={"verify_signature": False})
        keycloak_user = KeyCloakUser(**decoded_keycloak_token)
        access_token = create_access_token(data=keycloak_user)
        return access_token

    user_token = await get_token()
    response = RedirectResponse(url="/user_info/all")
    response.set_cookie("Authorization", value=f"Bearer {user_token}")
    return response


@router.get("/inspect")
async def validated(request: Request) -> ValidationJson:
    authorization: str = request.cookies.get("Authorization")
    scheme, user_token = get_authorization_scheme_param(authorization)
    validated = validate_user_token(user_token)
    return {"validated": validated}


@router.get("/info")
async def get_info(request: Request):
    authorization: str = request.cookies.get("Authorization")
    scheme, user_token = get_authorization_scheme_param(authorization)
    decoded = jwt.decode(user_token, settings.jwt_public_key, algorithms=settings.jwt_algorithm)
    return decoded