import os
from openai import AsyncOpenAI
from fastapi import HTTPException
from exceptions.api_exceptions import ApiError

async def get_openai_client():
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise HTTPException(
            status_code=ApiError.OPENAI_CLIENT_NOT_INITIALIZED[1],
            detail=ApiError.OPENAI_CLIENT_NOT_INITIALIZED[0]
        )
    
    try:
        client = AsyncOpenAI(api_key=openai_api_key)
        yield client
    except Exception:
        raise HTTPException(
            status_code=ApiError.OPENAI_CLIENT_NOT_INITIALIZED[1],
            detail=ApiError.OPENAI_CLIENT_NOT_INITIALIZED[0]
        )