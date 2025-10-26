from pydantic import BaseModel, Field

class AnkenInput(BaseModel):
    anken_detail: str = Field(..., min_length=1, description="案件の詳細（例: Javaを使用したテスト案件）。")
    negative_aspects: str = Field(..., min_length=1, description="不安や不満に感じている点（例: やりたい技術（React）と違う）。")
    shokumu_keireki: str = Field("", description="過去の経験言語、フレームワーク、ツール、担当した役割など。")

class ExplanationResponse(BaseModel):
    explanation: str = Field(..., description="AIによって生成されたポジティブな説明文。")