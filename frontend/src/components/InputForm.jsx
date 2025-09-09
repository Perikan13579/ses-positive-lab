import { useState } from 'react';
import Button from './common/Button';
import { ERROR_MESSAGES } from '../constants/messages';

function InputForm({ onGenerate, isLoading, apiError }) {
  const [ankenDetail, setAnkenDetail] = useState('');
  const [negativeAspects, setNegativeAspects] = useState('');
  const [shokumuKeireki, setShokumuKeireki] = useState('');
  const [errors, setErrors] = useState({});

  const validateInputs = () => {
    const newErrors = {};
    if (!ankenDetail.trim()) {
      newErrors.ankenDetail = ERROR_MESSAGES.REQUIRED_ANKEN_DETAIL;
    }
    if (!negativeAspects.trim()) {
      newErrors.negativeAspects = ERROR_MESSAGES.REQUIRED_NEGATIVE_ASPECTS;
    }
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleBlur = (field, value) => {
    if (!value.trim()) {
      let errorMessage = '';
      if (field === 'ankenDetail') {
        errorMessage = ERROR_MESSAGES.REQUIRED_ANKEN_DETAIL;
      }else if (field === 'negativeAspects') {
        errorMessage = ERROR_MESSAGES.REQUIRED_NEGATIVE_ASPECTS;
      }
      setErrors((prevErrors) => ({ ...prevErrors, [field]: errorMessage }));
    } else {
      setErrors((prevErrors) => {
        const updatedErrors = { ...prevErrors };
        delete updatedErrors[field];
        return updatedErrors;
      });
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (validateInputs()) {
      onGenerate({ ankenDetail, negativeAspects, shokumuKeireki });
    }
  };

  return (
    <section className="input-section">
      <h2>案件情報を入力して、新しい視点を見つけよう！</h2>
      <form onSubmit={handleSubmit}>
        <p className="warning-message">
          ⚠️氏名や個人情報、機密情報は入力しないでください。
        </p>

        <div className="form-group">
          <label htmlFor="ankenDetail">1. どのような案件ですか？ (必須)</label>
          <textarea
            id="ankenDetail"
            value={ankenDetail}
            onChange={(e) => setAnkenDetail(e.target.value)}
            onBlur={(e) => handleBlur('ankenDetail', e.target.value)}
            placeholder="例：Javaを使用したテスト案件、など、案件について入力してください。"
            rows={7}
          ></textarea>
          {errors.ankenDetail && <p className="error-message">{errors.ankenDetail}</p>}
        </div>

        <div className="form-group">
          <label htmlFor="negativeAspects">2. 今回の案件、正直どこが嫌ですか？ (必須)</label>
          <textarea
            id="negativeAspects"
            value={negativeAspects}
            onChange={(e) => setNegativeAspects(e.target.value)}
            onBlur={(e) => handleBlur('negativeAspects', e.target.value)}
            placeholder="例：やりたい技術（React）と違う、通勤時間が長い、など、不安や不満に感じている点を記述してください。"
            rows={7}
          ></textarea>
          {errors.negativeAspects && <p className="error-message">{errors.negativeAspects}</p>}
        </div>

        <div className="form-group">
          <label htmlFor="shokumuKeireki">3. あなたの職務経歴 (任意)</label>
          <textarea
            id="shokumuKeireki"
            value={shokumuKeireki}
            onChange={(e) => setShokumuKeireki(e.target.value)}
            onBlur={(e) => handleBlur('shokumuKeireki', e.target.value)}
            placeholder="過去の経験言語、フレームワーク、ツール、担当した役割などを記述してください。ポジティブな説明の精度を高めるため、できるだけ詳細に入力してください。"
            rows={5}
          ></textarea>
        </div>
        
        {apiError && <p className="error-message">{apiError}</p>}
        <Button type="submit" disabled={isLoading}>
          {isLoading ? 'AIが分析中…' : 'AIにポジティブな説明を生成してもらう'}
        </Button>
      </form>
    </section>
  );
}

export default InputForm;