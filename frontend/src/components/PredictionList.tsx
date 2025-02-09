import React, { useEffect, useState } from 'react';
import PredictionCard from './PredictionCard';
import { Prediction } from '../types';
import { predictionApi } from '../services/api';

const PredictionList: React.FC = () => {
  const [predictions, setPredictions] = useState<Prediction[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchPredictions();
  }, []);

  const fetchPredictions = async () => {
    try {
      const data = await predictionApi.getAllPredictions();
      setPredictions(data);
    } catch (err) {
      setError('Failed to load predictions');
      console.error('Error fetching predictions:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateAIPrediction = async () => {
    try {
      setLoading(true);
      const newPrediction = await predictionApi.getAIPrediction('BTC');
      await fetchPredictions(); // 重新获取所有预测
    } catch (err) {
      console.error('Error creating AI prediction:', err);
      setError('Failed to create AI prediction');
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div className="text-red-500">{error}</div>;

  return (
    <div>
      <div className="mb-4">
        <button
          onClick={handleCreateAIPrediction}
          className="bg-green-500 text-white px-4 py-2 rounded"
        >
          Generate AI Prediction
        </button>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <h2 className="text-xl font-bold mb-4">AI Predictions</h2>
          {predictions
            .filter(p => p.predictorType === 'AI')
            .map(prediction => (
              <PredictionCard key={prediction.id} prediction={prediction} isAI={true} />
            ))}
        </div>
        <div>
          <h2 className="text-xl font-bold mb-4">KOL Predictions</h2>
          {predictions
            .filter(p => p.predictorType === 'KOL')
            .map(prediction => (
              <PredictionCard key={prediction.id} prediction={prediction} isAI={false} />
            ))}
        </div>
      </div>
    </div>
  );
};

export default PredictionList;