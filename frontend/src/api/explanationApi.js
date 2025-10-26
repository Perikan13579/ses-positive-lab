import { apiClient } from './apiClient';

const EXPLANATION_ENDPOINT = '/api/v1/explanations/'; 

/**
 * AIによるポジティブな説明を生成する機能のラッパー関数。
 * @param {object} inputData - { anken_detail, negative_aspects, shokumu_keireki }
 * @returns {Promise<string>} 生成された説明文 (explanation フィールドのみ)
 * @throws {Error} API クライアントからスローされたエラー
 */
export async function generateExplanation(inputData) {
    const data = await apiClient.post(EXPLANATION_ENDPOINT, inputData);
    
    return data.explanation; 
}