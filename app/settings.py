from pydantic import BaseSettings, Field, validator


class Settings(BaseSettings):
    realm: str = "Clients"
    env: str = Field("prod", env="ENV")
    app_interface: str = Field("0.0.0.0", env="APP_INTERFACE")
    app_port: int = Field(8000, env="APP_PORT")
    app_url: str = Field("0.0.0.0:8000", env="APP_URL")
    keycloak_addr: str = Field("http://127.0.0.1:8080", env="KEYCLOAK_ADDR")
    backend_client_id: str = Field("app", env="BACKEND_CLIENT_ID")  # change
    backend_client_secret: str = Field("", env="BACKEND_CLIENT_SECRET")  # change
    jwt_private_key: str = Field( "", env="JWT_PRIVATE_KEY")
    jwt_public_key: str = Field("", env="JWT_PUBLIC_KEY")
    jwt_secret_key: str = Field("example_key_super_secret", env="JWT_SECRET_KEY")
    jwt_algorithm: str = Field("RS256", env="JWT_ALGORITHM")

    class Config:
        env_file = '.env'


settings = Settings()
