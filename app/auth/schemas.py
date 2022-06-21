from pydantic import BaseModel


class Url(BaseModel):
    url: str


class AuthorizationResponse(BaseModel):
    session_state: str


class KeyCloakUser(BaseModel):
    name: str
    email: str
    sid: str


class ValidationJson(BaseModel):
    validated: str
    shit: int


class Token(BaseModel):
    access_token: str
    token_type: str
    user: KeyCloakUser
