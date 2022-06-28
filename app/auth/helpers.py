from datetime import datetime, timedelta
import jwt
from app.settings import settings
from .schemas import KeyCloakUser

def create_access_token(*, data: KeyCloakUser, exp: int = None) -> bytes:
    to_encode = data.dict()
    if exp is not None:
        to_encode.update({"exp": exp})
    else:
        expire = datetime.utcnow() + timedelta(minutes=60)
        to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.jwt_private_key, algorithm=settings.jwt_algorithm
    )
    return encoded_jwt


def validate_user_token(encoded_user_token) -> bool:
    try:
        decoded = jwt.decode(encoded_user_token, settings.jwt_public_key, algorithms=settings.jwt_algorithm)
        output = True
    except Exception as e:
        print(e)
        output = False
    return output
