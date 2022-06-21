from pydantic import BaseSettings, Field, validator


class Settings(BaseSettings):
    realm: str = "Clients"
    env: str = Field("prod", env="ENV")
    app_interface: str = Field("127.0.0.1", env="APP_INTERFACE")
    app_port: int = Field(8000, env="APP_PORT")
    app_url: str = Field("127.0.0.1:8000", env="APP_URL")
    keycloak_addr: str = "http://127.0.0.1:8080"
    backend_client_id: str = Field("app", env="BACKEND_CLIENT_ID")  # change
    backend_client_secret: str = Field("CKLdegY4sk8MopiBuSv9ITnOOZAQWcEH", env="BACKEND_CLIENT_SECRET")  # change
    jwt_private_key: str = Field( b"-----BEGIN RSA PRIVATE KEY-----"
                                  b"\nMIIBOgIBAAJBAKCVE8ur1e5B9UkfCAqTmkn/mz/1m0FPsxi4wAAfzGqoBPbLcT4n"
                                  b"\nvJTCNv/r0nqi3lt11xmmu9uKOsnwqBxh6lMCAwEAAQJAWOKr1m0DOaKg1xyqItCY"
                                  b"\n8qTdloWornojNGfvPyJa0B3Xn9GEt4Sqb8mzkuLzwiZOo6sP/4K9VX/IvHOQZ5Cy"
                                  b"\n4QIhANsQbfb0DMYzDqIsL6zXD2HSBOL0NbMyVtdGyAQ1/gvlAiEAu6heSuMl33UQ"
                                  b"\noB05EMyFOcq4fGKB9vXU+nljxZxBadcCICP9ZAORftPFKZ9NIRwFTRqmFXVv566k"
                                  b"\nE45Uq6G9eRpdAiAdKpwNM6TNSFqfKCuYatFCHDn0SzM7+RVzIK7bJeAc3QIhAKXj"
                                  b"\nB+jMFxcx6Kx4N/WSpKkr/lGwqkKHYMo9KzpJV0Qr"
                                  b"\n-----END RSA PRIVATE KEY-----", env="JWT_PRIVATE_KEY")
    jwt_public_key: str = Field( b"-----BEGIN PUBLIC KEY-----"
                                 b"\nMFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAKCVE8ur1e5B9UkfCAqTmkn/mz/1m0FP"
                                 b"\nsxi4wAAfzGqoBPbLcT4nvJTCNv/r0nqi3lt11xmmu9uKOsnwqBxh6lMCAwEAAQ=="
                                 b"\n-----END PUBLIC KEY-----", env="JWT_PUBLIC_KEY")
    jwt_secret_key: str = Field("example_key_super_secret", env="JWT_SECRET_KEY")
    jwt_algorithm: str = Field("RS256", env="JWT_ALGORITHM")

    class Config:
        env_file = '.env'


settings = Settings()
