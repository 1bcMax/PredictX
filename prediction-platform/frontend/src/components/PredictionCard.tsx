import React, { useState } from 'react';
import { Prediction } from '../types';

interface Props {
  prediction: Prediction;
  isAI: boolean;
}

const formatPrice = (price: number) => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD'
  }).format(price);
};

const formatPercent = (value: number) => {
  return `${value > 0 ? '+' : ''}${value.toFixed(2)}%`;
};

const PredictionCard: React.FC<Props> = ({ prediction, isAI }) => {
  const [amount, setAmount] = useState("");
  const [isSupporting, setIsSupporting] = useState(false);
  
  const priceChange = prediction.predictedPrice - prediction.currentPrice;
  const priceChangePercent = (priceChange / prediction.currentPrice) * 100;
  
  return (
    <div className="border rounded-lg p-4 bg-white shadow mb-4">
      <div className="flex justify-between items-center mb-2">
        <h3 className="text-lg font-semibold">{prediction.asset}/USD</h3>
        <span className="text-sm text-gray-500">
          {isAI ? 'AI Prediction' : 'KOL Prediction'}
        </span>
      </div>
      
      {/* Current Price */}
      <div className="mb-4">
        <p className="text-sm text-gray-600">Current Price</p>
        <p className="text-xl font-bold">{formatPrice(prediction.currentPrice)}</p>
      </div>
      
      {/* Predicted Price */}
      <div className="mb-4">
        <p className="text-sm text-gray-600">Predicted Price (24h)</p>
        <p className={`text-xl font-bold ${priceChange >= 0 ? 'text-green-600' : 'text-red-600'}`}>
          {formatPrice(prediction.predictedPrice)}
          <span className="text-sm ml-2">
            ({formatPercent(priceChangePercent)})
          </span>
        </p>
      </div>
      
      {/* Market Data */}
      {prediction.marketData && (
        <div className="grid grid-cols-2 gap-4 mb-4 text-sm">
          <div>
            <p className="text-gray-600">24h Volume</p>
            <p className="font-medium">{formatPrice(prediction.marketData.volume_24h)}</p>
          </div>
          <div>
            <p className="text-gray-600">Market Cap</p>
            <p className="font-medium">{formatPrice(prediction.marketData.market_cap)}</p>
          </div>
          <div>
            <p className="text-gray-600">24h Change</p>
            <p className={`font-medium ${prediction.marketData.percent_change_24h >= 0 ? 'text-green-600' : 'text-red-600'}`}>
              {formatPercent(prediction.marketData.percent_change_24h)}
            </p>
          </div>
          <div>
            <p className="text-gray-600">7d Change</p>
            <p className={`font-medium ${prediction.marketData.percent_change_7d >= 0 ? 'text-green-600' : 'text-red-600'}`}>
              {formatPercent(prediction.marketData.percent_change_7d)}
            </p>
          </div>
        </div>
      )}
      
      {/* Confidence Level */}
      <div className="mb-4">
        <p className="text-sm text-gray-600">Confidence Level</p>
        <div className="w-full bg-gray-200 h-2 rounded-full">
          <div 
            className="bg-blue-600 h-2 rounded-full"
            style={{ width: `${prediction.confidence * 100}%` }}
          />
        </div>
        <p className="text-sm mt-1">{(prediction.confidence * 100).toFixed(1)}%</p>
      </div>
      
      {/* Reasoning */}
      <div className="mb-4">
        <p className="text-sm text-gray-600">Analysis</p>
        <p className="mt-1">{prediction.reasoning}</p>
      </div>
      
      {/* Support Section */}
      <div className="mt-4 pt-4 border-t">
        <div className="flex gap-2">
          <input
            type="number"
            className="flex-1 border rounded px-3 py-2"
            placeholder="Enter amount"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
          />
          <button
            onClick={() => setIsSupporting(true)}
            disabled={isSupporting}
            className={`px-4 py-2 rounded text-white ${
              isSupporting ? 'bg-gray-400' : 'bg-blue-500 hover:bg-blue-600'
            }`}
          >
            Support
          </button>
        </div>
      </div>
    </div>
  );
};

export default PredictionCard;