from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    GOOGLE_CLIENT_ID: str 
    GOOGLE_CALLBACK_URI: str
    GOOGLE_CLIENT_SECRET: str
    RESPONSE_TYPE: str
    SCOPE: str
    STATE: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    
    @computed_field
    @property
    def REDIRECT_URI(self) -> str:
        return (
            f'https://accounts.google.com/o/oauth2/v2/auth?'
            f'client_id={self.GOOGLE_CLIENT_ID}&'
            f'redirect_uri={self.GOOGLE_CALLBACK_URI}&'
            f'response_type={self.RESPONSE_TYPE}&'
            f'scope={self.SCOPE}&state={self.STATE}'
        )


settings = Settings()