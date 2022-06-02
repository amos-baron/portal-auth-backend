from pydantic import BaseSettings, Field, validator


class Settings(BaseSettings):
    realm: str = "Clients"
    env: str = Field("prod", env="ENV")
    app_url: str = Field("127.0.0.1:8000", env="APP_URL")
    db_uri: str = Field(
        "postgresql://example:example@localhost:5432/postgres", env="DB_URI"
    )
    keycloak_addr : str = "http://127.0.0.1:8080"
    backend_client_id: str = "app"#Field("", env="BACKEND_CLIENT_ID")
    backend_client_secret: str = "CKLdegY4sk8MopiBuSv9ITnOOZAQWcEH" #Field("", env="BACKEND_CLIENT_SECRET")
    jwt_secret_key: str = Field("example_key_super_secret", env="JWT_SECRET_KEY")
    jwt_algorithm: str = Field("HS256", env="JWT_ALGORITHM")

    class Config:
        env_file = '.env'

settings = Settings()