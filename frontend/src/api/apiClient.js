import { ERROR_MESSAGES } from '../constants/messages';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

/**
 * 汎用的な API クライアント関数。
 * バックエンドとの通信を行い、レスポンスを処理し、エラーを適切なメッセージに変換する。
 * * @param {string} endpoint - API のエンドポイントパス (例: '/api/v1/explanations')
 * @param {string} method - HTTP メソッド (例: 'POST', 'GET')
 * @param {object} [data=null] - リクエストボディとして送信するデータ
 * @returns {Promise<object>} API から返された JSON データ全体
 * @throws {Error} ユーザー向けの適切なエラーメッセージ
 */
async function callApi(endpoint, method, data = null) {
    const url = API_BASE_URL + endpoint;
    const config = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        },
    };
    // POST/PUTリクエストの場合、JSONボディを設定
    if (data) {
        config.body = JSON.stringify(data);
    }

    try {
        const response = await fetch(url, config);
        let responseData;
        
        // レスポンスボディをJSONとしてパースする (パース失敗も考慮)
        try {
             responseData = await response.json();
        } catch {
             responseData = {};
        }

        // HTTPステータスコードが 2xx 以外の場合、エラーとして処理
        if (!response.ok) {
            // FastAPIのバリデーションエラー形式の場合
            if (responseData.detail && Array.isArray(responseData.detail)) {
                throw new Error(ERROR_MESSAGES.API_VALIDATION_ERROR);
            } 
            // バックエンドからカスタムエラーメッセージが返された場合 (例: ApiError)
            else if (responseData.detail) {
                throw new Error(responseData.detail);
            } 
            // その他の不明なサーバーエラーの場合
            else {
                throw new Error(ERROR_MESSAGES.API_UNKNOWN_ERROR);
            }
        }
        
        return responseData;
    } catch (error) {
        // ネットワークエラー (サーバーがダウンしている、CORS設定ミスなど) の処理
        if (error.message === 'Failed to fetch' || error instanceof TypeError) {
             throw new Error(ERROR_MESSAGES.API_COMMUNICATION_ERROR);
        }
        // それ以外の、すでに適切なメッセージに変換されているエラーを再スロー
        throw error;
    }
}

export const apiClient = {
    post: (endpoint, data) => callApi(endpoint, 'POST', data),
    get: (endpoint) => callApi(endpoint, 'GET'),
    // 必要に応じて put, delete などを追加可能
};