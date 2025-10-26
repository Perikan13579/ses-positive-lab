from functools import lru_cache
from openai import AsyncOpenAI
from core.config import settings
from exceptions.api_exceptions import ApiError 
from constants.messages import ErrorMessages

# @lru_cache() を使用してクライアントをシングルトンとしてキャッシュする
@lru_cache()
def get_openai_client() -> AsyncOpenAI:
    """設定からAPIキーを使用してAsyncOpenAIクライアントを初期化し、キャッシュする。"""
    try:
        return AsyncOpenAI(
            api_key=settings.OPENAI_API_KEY
        )
    except Exception as e:
        # クライアント初期化時のエラーはカスタムApiErrorとしてラップする
        raise ApiError(
            status_code=500, 
            detail=f"{ErrorMessages.CLIENT_INIT_ERROR} {type(e).__name__}: {str(e)}"
        )

def get_openai_client_dependency() -> AsyncOpenAI:
    """FastAPIのDependsで使用するためのラッパー関数。"""
    return get_openai_client()