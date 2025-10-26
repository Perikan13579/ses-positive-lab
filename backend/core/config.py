from pydantic_settings import BaseSettings
from pydantic import Field
import os
from constants.messages import SystemMessages

# Docker Secretがマウントされるパスを定義
DOCKER_SECRET_PATH = "/run/secrets/openai_api_key"

class Settings(BaseSettings):
    """アプリケーション全体の設定を管理するクラス。環境変数またはDocker Secretから値を読み込む。"""

    OPENAI_API_KEY: str = Field(
        default="", 
        description="OpenAI APIキー (環境変数、Docker Secretがない場合のフォールバック)"
    )

    OPENAI_MODEL: str = "gpt-3.5-turbo"
    OPENAI_TEMPERATURE: float = 0.7
    OPENAI_MAX_TOKENS: int = 1000

    ADJUST_PROMPT_FOR_EMPTY_SHOKUMU: bool = True 
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs) 

        # OPENAI_API_KEYが設定されていない場合、Docker Secretから読み込みを試みる
        if not self.OPENAI_API_KEY:
            if os.path.exists(DOCKER_SECRET_PATH):
                try:
                    with open(DOCKER_SECRET_PATH, 'r') as f:
                        key = f.read().strip()
                        if key:
                            self.OPENAI_API_KEY = key 
                except Exception:
                    # Docker Secretの読み込みに失敗した場合、キーは空のまま続行
                    pass

        # 最終的にキーが設定されていない場合は例外を発生させる
        if not self.OPENAI_API_KEY:
            raise ValueError(SystemMessages.OPENAI_KEY_NOT_CONFIGURED)

settings = Settings()