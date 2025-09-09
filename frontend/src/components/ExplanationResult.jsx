import Button from './common/Button';

function ExplanationResult({ explanation, onReset }) {
  return (
    <section className="result-section">
      <h2>あなたの案件から見つかった、新しい可能性！</h2>
      <div className="explanation-box">
        <p>{explanation}</p>
      </div>
      <Button onClick={onReset}>
        もう一度、別の案件で試す
      </Button>
    </section>
  );
}

export default ExplanationResult;