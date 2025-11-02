import os
import openai
from fastapi import FastAPI, HTTPException, Depends, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from core.config import settings 
from exceptions.api_exceptions import ApiError
from api.v1.explanation import router as explanation_router 
from constants.messages import SystemMessages

REACT_APP_API_BASE_URL="REACT_APP_API_BASE_URL"

# FastAPIアプリケーションのメインインスタンスを初期化
app = FastAPI(
    title="SES AI Positive Explanation API",
    description="SES案件のネガティブな側面をポジティブに変換するAIサービス。",
    version="1.0.0",
)

# CORSミドルウェアを設定。開発環境のため全てのオリジンを許可している
origins = [
    os.environ.get(REACT_APP_API_BASE_URL)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# カスタム定義したApiErrorの例外ハンドラ
@app.exception_handler(ApiError)
async def api_error_exception_handler(request: Request, exc: ApiError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

# OpenAI API特有のエラー (APIError) の例外ハンドラ
@app.exception_handler(openai.APIError)
async def openai_api_error_handler(request: Request, exc: openai.APIError):
    # OpenAIのエラーはサーバー側の問題として 500 を返す
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": f"OpenAI API error: {exc.message}"},
    )

# 説明生成ルーターを登録
app.include_router(explanation_router, prefix="/api/v1/explanations") 

# ヘルスチェックエンドポイント
@app.get("/")
async def read_root():
    """アプリケーションが正常に動作していることを確認する。"""
    return {"message": SystemMessages.HEALTH_CHECK_SUCCESS}