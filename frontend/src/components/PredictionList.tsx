import React, { useEffect, useState } from 'react';
import { CdpAgentkit } from '@coinbase/agentkit';
import PredictionCard from './PredictionCard';
import { usePredictions } from '../hooks/usePredictions';

interface Props {
  agentkit: CdpAgentkit;
}

const PredictionList: React.FC<Props> = ({ agentkit }) => {
  const { predictions, loading, error, createAIPrediction } = usePredictions(agentkit);

  const handleCreatePrediction = async () => {
    try {
      await createAIPrediction('BTC');
    } catch (err) {
      console.error('Error creating prediction:', err);
    }
  };

  if (loading) return <div>Loading predictions...</div>;
  if (error) return <div className="text-red-500">{error}</div>;

  return (
    <div>
      <div className="mb-4">
        <button
          onClick={handleCreatePrediction}
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        >
          Generate New Prediction
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {predictions.map(prediction => (
          <PredictionCard 
            key={prediction.id}
            prediction={prediction}
            agentkit={agentkit}
          />
        ))}
      </div>
    </div>
  );
};

export default PredictionList;