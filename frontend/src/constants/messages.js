export const ERROR_MESSAGES = {
  REQUIRED_ANKEN_DETAIL: '案件情報は必須項目です。',
  REQUIRED_NEGATIVE_ASPECTS: '案件への嫌な点は必須項目です。',
  API_COMMUNICATION_ERROR: '通信中に予期せぬエラーが発生しました。時間を置いて再度お試しください。',
  API_UNKNOWN_ERROR: '不明なエラーが発生しました。時間を置いて再度お試しください。', 
  API_VALIDATION_ERROR: '入力内容の検証に失敗しました。フォームの内容を再確認してください。',
};

export const UI_TEXTS = {
  // InputForm.jsx
  SECTION_TITLE: '案件について入力して、新しい視点を見つけよう！',
  WARNING_MESSAGE: '⚠️氏名や個人情報、機密情報は入力しないでください。',
  ANKEN_LABEL: '1. どのような案件ですか？ (必須)',
  NEGATIVE_ASPECTS_LABEL: '2. 今回の案件、正直どこが嫌ですか？ (必須)',
  SHOKUMU_LABEL: '3. あなたの職務経歴 (任意)',
  ANKEN_PLACEHOLDER: '例：Javaを使用したテスト案件、など、案件について入力してください。',
  NEGATIVE_ASPECTS_PLACEHOLDER: '例：やりたい技術（React）と違う、通勤時間が長い、など、不安や不満に感じている点を記述してください。',
  SHOKUMU_PLACEHOLDER: '過去の経験言語、フレームワーク、ツール、担当した役割などを記述してください。ポジティブな説明の精度を高めるため、できるだけ詳細に入力してください。',
  GENERATE_BUTTON_TEXT: 'AIにポジティブな説明を生成してもらう',
  LOADING_MESSAGE: 'AIが分析中…',

  // App.jsx
  APP_HEADER_TITLE: 'SES案件ポジティブ説明アプリ',
  APP_FOOTER_COPYRIGHT: '© 2025 ペリカンうずら',

  // ExplanationResult.jsx
  RESULT_SECTION_TITLE: 'あなたの案件から見つかった、新しい可能性！',
  RESULT_RESET_BUTTON: 'もう一度、別の案件で試す',
};