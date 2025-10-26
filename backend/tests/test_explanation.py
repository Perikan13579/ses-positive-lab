import pytest
from httpx import AsyncClient
from unittest.mock import MagicMock
from openai import AuthenticationError, RateLimitError
from constants.messages import SystemMessages, ErrorMessages
from schemas import ExplanationResponse

# --------------------------------------------------
# 説明生成エンドポイントのテスト
# --------------------------------------------------

@pytest.mark.asyncio
async def test_create_explanation_success(client: AsyncClient, mock_openai_client, anken_input_data: dict, expected_explanation_text: str):
    """説明生成APIのテスト (正常系: OpenAIとの連携が成功)"""
    response = await client.post("/api/v1/explanations/", json=anken_input_data)

    assert response.status_code == 200
    
    # レスポンスが期待されるスキーマ (ExplanationResponse) に準拠していることを確認
    ExplanationResponse(**response.json())
    
    # 返された説明文がモックで設定したものと一致することを確認
    assert response.json()["explanation"] == expected_explanation_text
    
    # モックのOpenAIクライアントが一度だけ呼び出されたことを確認 (重要なテスト)
    mock_openai_client.chat.completions.create.assert_called_once()
    
    # 呼び出し時に渡されたプロンプトの構成を簡単に確認
    args, kwargs = mock_openai_client.chat.completions.create.call_args
    messages = kwargs['messages']
    assert messages[0]['role'] == 'system'
    assert 'SES営業担当者' in messages[0]['content'] # System Promptの一部を確認

@pytest.mark.asyncio
async def test_create_explanation_validation_error(client: AsyncClient, anken_input_data: dict):
    """入力データ不足によるバリデーションエラーのテスト (異常系: 必須項目なし)"""
    # 案件詳細を意図的に空にする
    invalid_data = anken_input_data.copy()
    invalid_data["anken_detail"] = "" 
    
    response = await client.post("/api/v1/explanations/", json=invalid_data)
    
    # FastAPIのバリデーションエラーのステータスコード 422 を確認
    assert response.status_code == 422 
    # エラー詳細に "anken_detail" が含まれていることを確認
    assert "anken_detail" in response.json()["detail"][0]["loc"]

@pytest.mark.asyncio
async def test_create_explanation_openai_auth_error(client: AsyncClient, mock_openai_client, anken_input_data: dict):
    """OpenAI API認証エラーのテスト (異常系: APIキー不正)"""
    
    mock_openai_client.chat.completions.create.side_effect = AuthenticationError(
        message="Invalid key", 
        response=MagicMock(),
        body={"message": "Invalid key"},
    )

    response = await client.post("/api/v1/explanations/", json=anken_input_data)

@pytest.mark.asyncio
async def test_read_root_health_check(client: AsyncClient):
    """ヘルスチェックエンドポイントのテスト (正常系)"""
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == SystemMessages.HEALTH_CHECK_SUCCESS