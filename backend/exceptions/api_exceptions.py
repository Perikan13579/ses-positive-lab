from fastapi import status

class ApiError:
    OPENAI_API_KEY_NOT_SET = "OpenAI API Key is not set. Please set the OPENAI_API_KEY environment variable."

    API_CONNECTION_ERROR = ("APIへの接続に失敗しました。時間をおいてお試しください。", status.HTTP_503_SERVICE_UNAVAILABLE)
    RATE_LIMIT_ERROR = ("APIへのリクエストが多すぎます。時間をおいてお試しください。", status.HTTP_429_TOO_MANY_REQUESTS)
    OPENAI_API_STATUS_ERROR = ("AIモデルの処理中にエラーが発生しました。時間をおいてお試しください。", status.HTTP_500_INTERNAL_SERVER_ERROR)
    UNEXPECTED_ERROR = ("AI生成中に予期せぬエラーが発生しました。", status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    OPENAI_CLIENT_NOT_INITIALIZED = ("OpenAI client is not initialized.", status.HTTP_500_INTERNAL_SERVER_ERROR)