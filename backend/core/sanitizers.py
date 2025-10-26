import spacy
import re

# 日本語のspaCyモデルをロード
try:
    nlp = spacy.load("ja_core_news_sm")
except ImportError:
    raise ImportError("ja_core_news_smモデルがインストールされていません。'python -m spacy download ja_core_news_sm'を実行してください。")

def sanitize_text(text: str) -> str:
    """
    入力テキストから個人情報や機密情報と推定されるエンティティをマスクします。

    Args:
        text (str): サニタイズ対象の入力テキスト。

    Returns:
        str: 機密情報がプレースホルダーに置換されたテキスト。
    """

    if not isinstance(text, str):
        # 文字列でない場合はそのまま返す
        return text

    doc = nlp(text)
    sanitized_text = text

    # マスク対象のエンティティと置換後のプレースホルダーのマップ
    entities_to_mask = {
        "PERSON": "[氏名]",
        "ORG": "[組織名]",
        "GPE": "[地名]",
        "PRODUCT": "[製品名]",
    }

    # spaCyによる固有表現認識 (NER) を使用し、検出されたエンティティを置換
    # 文字列置換のインデックスを維持するため、エンティティを逆順に処理する
    for ent in reversed(doc.ents):
        if ent.label_ in entities_to_mask:
            placeholder = entities_to_mask[ent.label_]
            sanitized_text = sanitized_text[:ent.start_char] + placeholder + sanitized_text[ent.end_char:]
            
    # 正規表現を使用してメールアドレスと電話番号をマスク
    sanitized_text = re.sub(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', '[メールアドレス]', sanitized_text)
    sanitized_text = re.sub(r'\b\d{2,4}-\d{2,4}-\d{4}\b', '[電話番号]', sanitized_text)
    
    return sanitized_text