import pytest
import asyncio
from httpx import AsyncClient, ASGITransport
from unittest.mock import MagicMock, patch, AsyncMock
from main import app
from core.config import settings
from api.v1.explanation import get_openai_client_dependency

# --------------------------------------------------
# FastAPIテストクライアントのフィクスチャ
# --------------------------------------------------
@pytest.fixture(scope="function")
def anyio_backend():
    """pytest-asyncioが使用する非同期バックエンドを指定"""
    return "asyncio"

@pytest.fixture(scope="function")
def client(request, mock_openai_client):
    """
    アプリケーションに対してHTTPリクエストを送信するためのテスト専用クライアントを提供
    """
    # config.pyでValueErrorが発生しないように、モックのAPIキーを設定
    settings.OPENAI_API_KEY = "dummy-key-for-test"

    # テスト中は、実際のクライアントではなくモッククライアントを使用するようDIを上書き
    app.dependency_overrides[get_openai_client_dependency] = lambda: mock_openai_client
    
    # AsyncClient を初期化
    ac = AsyncClient(transport=ASGITransport(app=app), base_url="http://test")

    # クリーンアップ関数を定義
    def finalizer():
        # テスト終了後、非同期の ac.aclose() を同期的に実行して確実に閉じる
        asyncio.run(ac.aclose()) 
    
    # テスト終了時に finalizer を実行するよう登録
    request.addfinalizer(finalizer)

    # クライアントオブジェクトを yield する
    yield ac

# --------------------------------------------------
# OpenAIクライアントのモックフィクスチャ
# --------------------------------------------------
@pytest.fixture
def mock_openai_client():
    """AsyncOpenAIクライアントのモックオブジェクト"""
    mock_client = AsyncMock()
    
    # 正常系レスポンスのモック設定
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "これはAIが生成したポジティブな説明文です。"
    
    # chat.completions.create の返り値を設定
    mock_client.chat.completions.create.return_value = mock_response
    
    # get_openai_client_dependencyがこのモックを返すようにパッチを適用
    with patch("api.v1.explanation.get_openai_client_dependency", return_value=mock_client) as mock_dep:
        yield mock_client # テスト関数にモッククライアントを渡す

# --------------------------------------------------
# テスト用固定データ
# --------------------------------------------------
@pytest.fixture
def anken_input_data():
    """APIリクエストのテストデータ"""
    return {
        "anken_detail": "テストのためにJavaで3年間テストをします。地味な作業が多いです。",
        "negative_aspects": "モダンな技術(React, Vue)が使えないのが嫌です。",
        "shokumu_keireki": "過去にWeb開発でJavaScript, Pythonの使用経験があります。"
    }

@pytest.fixture
def expected_explanation_text():
    """モッククライアントが返す想定のポジティブ説明文"""
    return "これはAIが生成したポジティブな説明文です。"