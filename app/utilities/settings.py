from pydantic import (
    BaseSettings,
    Field,
)


class Settings(BaseSettings):
    app_name: str = Field(env="APP_NAME")
    app_description: str = Field(env="APP_DESC")
    app_version: str = Field(env="APP_VERSION")
    memcached_host: str = Field(env="MEMCAHED_HOST")
    memcached_port: int = Field(env="MEMCAHED_PORT")
    memcached_prefix: str = Field(env="MEMCAHED_PREFIX")

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        case_sensitive = True
