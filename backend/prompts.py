class Prompts:

    # 1. システムプロンプト (AIの役割定義)
    SYSTEM_PROMPT: str = (
        "あなたは、SES営業担当者をサポートするプロのポジティブ変換AIです。"
        "ユーザーが提供するネガティブな案件情報や不満点を、"
        "その案件のポジティブな側面、長期的なキャリアパス、または隠れた利点に変換するよう、説得力のある説明文を生成します。"
        "回答は日本語で行い、フレンドリーかつプロフェッショナルなトーンで統一してください。"
        "生成する説明文は、単なるポジティブな言葉の羅列ではなく、具体的なキャリアメリットを提示するものとします。"
    )

    # 2. ユーザープロンプトのテンプレート (整形前のテンプレート)
    USER_INPUT_TEMPLATE: str = """
## 案件情報
案件詳細: {anken_detail}
不満点: {negative_aspects}

## 職務経歴
{shokumu_keireki_text}

## 依頼事項
上記の案件情報と不満点、そして職務経歴を踏まえ、この案件に参画することのメリットを最大限に引き出した、ポジティブで説得力のある説明文を生成してください。
"""

    @staticmethod
    def format_user_input(
        anken_detail: str,
        negative_aspects: str,
        shokumu_keireki: str
    ) -> str:
        if not shokumu_keireki:
            shokumu_keireki_text = "職務経歴は提供されていません。"
        else:
            shokumu_keireki_text = f"経験情報: {shokumu_keireki}"

        return Prompts.USER_INPUT_TEMPLATE.format(
            anken_detail=anken_detail,
            negative_aspects=negative_aspects,
            shokumu_keireki_text=shokumu_keireki_text,
        ).strip()