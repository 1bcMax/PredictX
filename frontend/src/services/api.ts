import axios from 'axios';
import { Prediction } from '../types';

const API_URL = 'http://localhost:8000';

export const predictionApi = {
  getAllPredictions: async (): Promise<Prediction[]> => {
    const response = await axios.get(`${API_URL}/predictions`);
    return response.data;
  },

  getAIPrediction: async (asset: string): Promise<Prediction> => {
    const response = await axios.post(`${API_URL}/predictions/ai`, {
      asset: asset
    });
    return response.data;
  },

  createKOLPrediction: async (prediction: Omit<Prediction, 'id'>): Promise<Prediction> => {
    const response = await axios.post(`${API_URL}/predictions/kol`, prediction);
    return response.data;
  },

  supportPrediction: async (
    predictionId: number,
    amount: number,
    supportAi: boolean
  ) => {
    const response = await axios.post(`${API_URL}/support`, {
      predictionId,
      amount,
      supportAi
    });
    return response.data;
  }
};