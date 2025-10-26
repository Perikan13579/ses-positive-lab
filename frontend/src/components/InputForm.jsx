import PropTypes from 'prop-types';
import { useState } from 'react';
import Button from './common/Button';
import { ERROR_MESSAGES, UI_TEXTS } from '../constants/messages'; 

function InputForm({ onGenerate, isLoading, apiError }) {
  // 各フォーム入力フィールドのローカルステートを管理
  const [ankenDetail, setAnkenDetail] =useState('');
  const [negativeAspects, setNegativeAspects] = useState('');
  const [shokumuKeireki, setShokumuKeireki] = useState('');
  const [errors, setErrors] = useState({}); // 入力検証エラーメッセージを管理

  /**
   * フォーム送信前に必須フィールドの検証を行う。
   * @returns {boolean} バリデーションが成功したかどうか
   */
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

  /**
   * フィールドからフォーカスが外れた時 (onBlur) のエラー表示/非表示を処理する。
   * shokumuKeirekiは任意項目なので検証しない。
   */
  const handleBlur = (field, value) => {
    if (!value.trim() && (field === 'ankenDetail' || field === 'negativeAspects')) {
      let errorMessage = '';
      if (field === 'ankenDetail') {
        errorMessage = ERROR_MESSAGES.REQUIRED_ANKEN_DETAIL;
      }else if (field === 'negativeAspects') {
        errorMessage = ERROR_MESSAGES.REQUIRED_NEGATIVE_ASPECTS;
      }
      setErrors((prevErrors) => ({ ...prevErrors, [field]: errorMessage }));
    } else {
      // 値が入力されたらエラーをクリア
      setErrors((prevErrors) => {
        const updatedErrors = { ...prevErrors };
        delete updatedErrors[field];
        return updatedErrors;
      });
    }
  };

  /**
   * フォーム送信時のハンドラ。バリデーション後に親コンポーネントの生成関数を呼び出す。
   */
  const handleSubmit = (e) => {
    e.preventDefault();
    if (validateInputs()) {
      onGenerate({ 
        anken_detail: ankenDetail.trim(), 
        negative_aspects: negativeAspects.trim(), 
        shokumu_keireki: shokumuKeireki.trim(),
      });
    }
  };

  return (
    <section className="input-section">
      <h2>{UI_TEXTS.SECTION_TITLE}</h2>
      <form onSubmit={handleSubmit}>
        <p className="warning-message">
          {UI_TEXTS.WARNING_MESSAGE}
        </p>

        {/* 1. 案件詳細の入力フィールド */}
        <div className="form-group">
          <label htmlFor="ankenDetail">{UI_TEXTS.ANKEN_LABEL}</label>
          <textarea
            id="ankenDetail"
            value={ankenDetail}
            onChange={(e) => setAnkenDetail(e.target.value)}
            onBlur={(e) => handleBlur('ankenDetail', e.target.value)}
            placeholder={UI_TEXTS.ANKEN_PLACEHOLDER}
            rows={7}
          ></textarea>
          {/* バリデーションエラーメッセージの表示 */}
          {errors.ankenDetail &&<p className="error-message">{errors.ankenDetail}</p>}
        </div>

        {/* 2. 不満点の入力フィールド */}
        <div className="form-group">
          <label htmlFor="negativeAspects">{UI_TEXTS.NEGATIVE_ASPECTS_LABEL}</label>
          <textarea
            id="negativeAspects"
            value={negativeAspects}
            onChange={(e) =>setNegativeAspects(e.target.value)}
            onBlur={(e) => handleBlur('negativeAspects', e.target.value)}
            placeholder={UI_TEXTS.NEGATIVE_ASPECTS_PLACEHOLDER}
            rows={7}
          ></textarea>
          {errors.negativeAspects && <p className="error-message">{errors.negativeAspects}</p>}
        </div>

        {/* 3. 職務経歴の入力フィールド (任意) */}
        <div className="form-group">
          <label htmlFor="shokumuKeireki">{UI_TEXTS.SHOKUMU_LABEL}</label>
          <textarea
            id="shokumuKeireki"
            value={shokumuKeireki}
            onChange={(e) =>setShokumuKeireki(e.target.value)}
            onBlur={(e) => handleBlur('shokumuKeireki', e.target.value)}
            placeholder={UI_TEXTS.SHOKUMU_PLACEHOLDER}
            rows={5}
          ></textarea>
        </div>
        
        {/* API通信エラーの表示 */}
        {apiError && <p className="error-message">{apiError}</p>}
        
        {/* 送信ボタン */}
        <Button type="submit" disabled={isLoading}>
          {isLoading ? UI_TEXTS.LOADING_MESSAGE : UI_TEXTS.GENERATE_BUTTON_TEXT}
        </Button>
      </form>
    </section>
  );
}

// PropTypeの定義 (親コンポーネントからのpropsの型チェック)
InputForm.propTypes = {
  isLoading: PropTypes.bool.isRequired,
  apiError: PropTypes.string,
  onGenerate: PropTypes.func.isRequired,
};

export default InputForm;