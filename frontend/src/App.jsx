import { useState } from 'react';
import './App.css';
import InputForm from './components/InputForm';
import ExplanationResult from './components/ExplanationResult';
import { generateExplanation } from './api/explanationApi';
import { UI_TEXTS } from './constants/messages';

function App() {
  // AI生成結果、ロード状態、APIエラーの状態を管理
  const [explanation, setExplanation] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [apiError, setApiError] = useState(null);

  /**
   * 説明生成ボタンが押された時のハンドラ。
   * APIを呼び出し、結果またはエラーをステートに反映する。
   * * @param {object} inputData - 案件情報、不満点、職務経歴
   */
  const handleGenerate = async ({ anken_detail, negative_aspects, shokumu_keireki }) => {
    setIsLoading(true);
    setApiError(null); // 新しいリクエスト開始時にエラーをリセット
    setExplanation(''); // 新しいリクエスト開始時に結果をリセット
    const inputData = { anken_detail, negative_aspects, shokumu_keireki };

    try {
      const resultExplanation = await generateExplanation(inputData);
      setExplanation(resultExplanation); // 成功した結果をセット

    } catch (err) {
      setApiError(err.message); // エラーメッセージをセット
    } finally {
      setIsLoading(false); // 処理完了
    }
  };

  /**
   * リセットボタンが押された時のハンドラ。
   * 全ての状態を初期値に戻し、入力フォームに戻る。
   */
  const handleReset = () => {
    setExplanation('');
    setApiError(null);
  };
  
  return (
    <div className="App">
      <header className="App-header">
        <h1>{UI_TEXTS.APP_HEADER_TITLE}</h1>
      </header>
      <main className="App-main">
        {/* explanation が空の場合、入力フォームを表示 */}
        {!explanation ? (
          <InputForm
            onGenerate={handleGenerate}
            isLoading={isLoading}
            apiError={apiError}
          />
        ) : (
          /* explanation がある場合、結果画面を表示 */
          <ExplanationResult
            explanation={explanation}
            onReset={handleReset}
          />
        )}
      </main>
      <footer className="App-footer">
        <p>{UI_TEXTS.APP_FOOTER_COPYRIGHT}</p>
      </footer>
    </div>
  );
}

export default App;