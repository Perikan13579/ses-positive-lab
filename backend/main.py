import os
import openai
from fastapi import FastAPI, HTTPException, Depends, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Annotated
from core.dependencies import get_openai_client
from core.config import OpenAISettings
from prompts import Prompts
from exceptions.api_exceptions import ApiError
from openai import AsyncOpenAI
from core.sanitizers import sanitize_text

openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise RuntimeError(ApiError.OPENAI_API_KEY_NOT_SET)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(openai.APIConnectionError)
async def openai_connection_exception_handler(request: Request, exc: openai.APIConnectionError):
    return JSONResponse(
        status_code=ApiError.API_CONNECTION_ERROR[1],
        content={"detail": ApiError.API_CONNECTION_ERROR[0]}
    )

@app.exception_handler(openai.RateLimitError)
async def openai_rate_limit_exception_handler(request: Request, exc: openai.RateLimitError):
    return JSONResponse(
        status_code=ApiError.RATE_LIMIT_ERROR[1],
        content={"detail": ApiError.RATE_LIMIT_ERROR[0]}
    )
    
@app.exception_handler(openai.APIStatusError)
async def openai_status_exception_handler(request: Request, exc: openai.APIStatusError):
    return JSONResponse(
        status_code=ApiError.OPENAI_API_STATUS_ERROR[1],
        content={"detail": ApiError.OPENAI_API_STATUS_ERROR[0]}
    )

@app.exception_handler(Exception)
async def unexpected_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=ApiError.UNEXPECTED_ERROR[1],
        content={"detail": ApiError.UNEXPECTED_ERROR[0]}
    )

class AnkenInput(BaseModel):
    anken_detail: str = Field(..., description="Javaを使用したテスト案件、など、案件について入力してください。")
    negative_aspects: str = Field(..., description="やりたい技術（React）と違う、通勤時間が長い、など、不安や不満に感じている点を記述してください。")
    shokumu_keireki: str = Field("", description="過去の経験言語、フレームワーク、ツール、担当した役割などを記述してください。ポジティブな説明の精度を高めるため、できるだけ詳細に入力してください。")

@app.post("/explanations/")
async def create_explanation(
    input_data: AnkenInput,
    client: Annotated[AsyncOpenAI, Depends(get_openai_client)]
):
    system_prompt = Prompts.SYSTEM_PROMPT
    
    sanitized_anken_detail = sanitize_text(input_data.anken_detail)
    sanitized_negative_aspects = sanitize_text(input_data.negative_aspects)
    sanitized_shokumu_keireki = sanitize_text(input_data.shokumu_keireki)

    formatted_user_input = Prompts.format_user_input(
        sanitized_anken_detail,
        sanitized_negative_aspects,
        sanitized_shokumu_keireki
    )
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": formatted_user_input}
    ]

    response = await client.chat.completions.create(
        model=OpenAISettings.MODEL,
        messages=messages,
        temperature=OpenAISettings.TEMPERATURE,
        max_tokens=OpenAISettings.MAX_TOKENS
    )
    
    positive_explanation = response.choices[0].message.content
    return {"explanation": positive_explanation}

@app.get("/")
async def read_root():
    return {"message": "SES AI Positive Explanation API is running."}
