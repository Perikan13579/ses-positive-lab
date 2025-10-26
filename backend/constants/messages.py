# APIのエラーレスポンスとしてクライアントに返すメッセージ
class ErrorMessages:
    """クライアントに返されるAPIエラーメッセージを一元管理するクラス"""
    
    # 認証/設定エラー (HTTP 500)
    # クライアントへの伝達：サーバー設定のエラーであることを明確に伝える
    SERVER_CONFIG_AUTH_ERROR = "Server configuration error: The OpenAI API Key is missing or invalid. Please check the server secrets."
    
    # レート制限エラー (HTTP 429)
    RATE_LIMIT_EXCEEDED = "OpenAI rate limit exceeded. Please try again later."
    
    # 外部APIサービス利用不可エラー (HTTP 503)
    API_SERVICE_UNAVAILABLE = "OpenAI API service unavailable."
    
    # OpenAIクライアント初期化時のエラー (内部エラー、HTTP 500)
    CLIENT_INIT_ERROR = "OpenAI Client initialization error."

    # その他APIエラー (FastAPIのカスタムエラーApiError用)
    # これは具体的な内容を動的にセットするため、基本メッセージのみ
    API_GENERAL_ERROR = "An unexpected API error occurred."


# ロギングや内部処理で利用する、固定の定数
class SystemMessages:
    """システム内部で使用するログや固定の文字列"""
    
    # 依存性注入の際に使用する、OpenAIキー未設定時のエラーメッセージ
    OPENAI_KEY_NOT_CONFIGURED = "OpenAI API Key (Docker Secret or Environment Variable) is not configured."
    
    # ヘルスチェックの成功メッセージ
    HEALTH_CHECK_SUCCESS = "SES AI Positive Explanation API is running."