import Button from './common/Button';
import { UI_TEXTS } from '../constants/messages'; 

function ExplanationResult({ explanation, onReset }) {
  return (
    <section className="result-section">
      <h2>{UI_TEXTS.RESULT_SECTION_TITLE}</h2>
      <div className="explanation-box">
        <p>{explanation}</p>
      </div>
      <Button onClick={onReset}>
        {UI_TEXTS.RESULT_RESET_BUTTON}
      </Button>
    </section>
  );
}

export default ExplanationResult;