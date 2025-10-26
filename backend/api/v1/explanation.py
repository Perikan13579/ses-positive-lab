from fastapi import APIRouter, Depends, HTTPException, status 
from typing import Annotated
from openai import AsyncOpenAI, AuthenticationError, RateLimitError, APIError
from core.dependencies import get_openai_client_dependency 
from core.config import settings
from core.sanitizers import sanitize_text
from prompts import Prompts
from schemas import AnkenInput, ExplanationResponse
from constants.messages import ErrorMessages

router = APIRouter(
    tags=["explanations"],
)

@router.post("/", response_model=ExplanationResponse)
async def create_explanation(
    input_data: AnkenInput,
    # 依存性注入により、設定済みのAsyncOpenAIクライアントを取得
    client: Annotated[AsyncOpenAI, Depends(get_openai_client_dependency)] 
):
    """
    ユーザー入力に基づき、AIにポジティブな説明文を生成させます。

    Args:
        input_data (AnkenInput): 案件詳細、不満点、職務経歴を含む入力データ。
        client (AsyncOpenAI): OpenAI APIクライアントインスタンス。

    Returns:
        ExplanationResponse: AIが生成した説明文。
    """
    system_prompt = Prompts.SYSTEM_PROMPT
    
    # 入力データに含まれる機密情報（氏名、組織名など）をマスクするサニタイズ処理
    sanitized_anken_detail = sanitize_text(input_data.anken_detail)
    sanitized_negative_aspects = sanitize_text(input_data.negative_aspects)
    sanitized_shokumu_keireki = sanitize_text(input_data.shokumu_keireki)
    
    # AIへのプロンプトを整形
    formatted_user_input = Prompts.format_user_input(
        sanitized_anken_detail,
        sanitized_negative_aspects,
        sanitized_shokumu_keireki
    )
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": formatted_user_input}
    ]
    
    try:
        # OpenAI APIを非同期で呼び出し
        response = await client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=messages,
            temperature=settings.OPENAI_TEMPERATURE,
            max_tokens=settings.OPENAI_MAX_TOKENS
        )
    # 認証失敗 (APIキー不正) の例外処理
    except AuthenticationError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorMessages.SERVER_CONFIG_AUTH_ERROR
        )
    # レート制限超過の例外処理
    except RateLimitError:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=ErrorMessages.RATE_LIMIT_EXCEEDED
        )
    # その他のOpenAI APIエラーの例外処理
    except APIError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"{ErrorMessages.API_SERVICE_UNAVAILABLE}: {e.message}"
        )
    
    # AIのレスポンスから生成された説明文を抽出
    positive_explanation = response.choices[0].message.content
    
    return ExplanationResponse(explanation=positive_explanation)