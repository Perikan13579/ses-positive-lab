import { useState } from 'react';
import './App.css';
import InputForm from './components/InputForm';
import ExplanationResult from './components/ExplanationResult';

function App() {
  const [explanation, setExplanation] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [apiError, setApiError] = useState(null);

  const handleGenerate = async ({ ankenDetail, negativeAspects, shokumuKeireki }) => {
    setIsLoading(true);
    setApiError(null);
    setExplanation('');

    try {
      const response = await fetch('http://http://3.14.126.161:8000/explanations/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ anken_detail: ankenDetail, negative_aspects: negativeAspects, shokumu_keireki: shokumuKeireki }),
      });

      const data = await response.json();
      if (!response.ok) {
        setApiError(data.detail || '通信中に予期せぬエラーが発生しました。');
      } else {
        setExplanation(data.explanation);
      }
    } catch (err) {
      setApiError('通信中に予期せぬエラーが発生しました。時間を置いて再度お試しください。');
      console.error('API呼び出しエラー:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setExplanation('');
    setApiError(null);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>SES案件ポジティブ説明アプリ</h1>
      </header>
      <main className="App-main">
        {!explanation ? (
          <InputForm
            onGenerate={handleGenerate}
            isLoading={isLoading}
            apiError={apiError}
          />
        ) : (
          <ExplanationResult
            explanation={explanation}
            onReset={handleReset}
          />
        )}
      </main>
      <footer className="App-footer">
        <p>&copy; 2025 ペリカンうずら</p>
      </footer>
    </div>
  );
}

export default App;