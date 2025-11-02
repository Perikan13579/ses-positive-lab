import '@testing-library/jest-dom';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import InputForm from './InputForm'; 
import { UI_TEXTS, ERROR_MESSAGES } from '../constants/messages';

const mockOnSubmit = jest.fn();
const mockOnGenerate = jest.fn();

// InputFormが使用するButtonコンポーネントをモック化
jest.mock('./common/Button', () => ({ children, onClick, type }) => (
  // テスト内で要素を簡単に特定できるように data-testid を付与
  <button data-testid="submit-button" onClick={onClick} type={type}>
    {children}
  </button>
));


// ----------------------------------------------------------------------
// テストケース 1: 初期レンダリングの確認
// ----------------------------------------------------------------------
test('1. 初期状態で、すべての入力フィールドと警告メッセージが正しく表示されること', () => {
  render(<InputForm onSubmit={mockOnSubmit} isLoading={false} onGenerate={mockOnGenerate} />);

  // タイトルと警告メッセージの確認
  expect(screen.getByText(UI_TEXTS.SECTION_TITLE)).toBeInTheDocument();
  expect(screen.getByText(UI_TEXTS.WARNING_MESSAGE)).toBeInTheDocument();

  // 必須入力フィールドのラベル確認
  expect(screen.getByLabelText(UI_TEXTS.ANKEN_LABEL)).toBeInTheDocument();
  expect(screen.getByLabelText(UI_TEXTS.NEGATIVE_ASPECTS_LABEL)).toBeInTheDocument();
  
  // 任意入力フィールドのラベル確認
  expect(screen.getByLabelText(UI_TEXTS.SHOKUMU_LABEL)).toBeInTheDocument();

  // 送信ボタンの確認 (Buttonコンポーネントに '送信' というテキストが表示されることを前提)
  const expectedButtonName = 'AIにポジティブな説明を生成してもらう';
  expect(screen.getByRole('button', { name: expectedButtonName })).toBeInTheDocument();
});


// ----------------------------------------------------------------------
// テストケース 2: 必須検証エラーの確認
// ----------------------------------------------------------------------
test('2. 必須項目が空の状態で送信を試みると、検証エラーメッセージが表示されること', async () => {
  render(<InputForm onSubmit={mockOnSubmit} isLoading={false} onGenerate={mockOnGenerate} />);

  // 送信ボタンを取得しクリック (モックで付与した data-testid="submit-button" を使用)
  const submitButton = screen.getByTestId('submit-button');
  fireEvent.click(submitButton);

  // 検証ロジックの実行を待つ
  await waitFor(() => {
    // 必須項目のエラーメッセージが表示されたことを確認1
    expect(screen.getByText(ERROR_MESSAGES.REQUIRED_ANKEN_DETAIL)).toBeInTheDocument();
  });

  // 必須項目のエラーメッセージが表示されたことを確認2
  expect(screen.getByText(ERROR_MESSAGES.REQUIRED_NEGATIVE_ASPECTS)).toBeInTheDocument();

  // 必須項目が満たされていないため、onSubmit関数が呼ばれていないことを確認
  expect(mockOnSubmit).not.toHaveBeenCalled();
});