from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "FraudLens"
    app_version: str = "0.1.0"
    app_env: str = "development"

    cognodb_uri: str = ""
    cognodb_username: str = ""
    cognodb_password: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()