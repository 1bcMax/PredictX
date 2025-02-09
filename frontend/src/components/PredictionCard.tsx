import React, { useState } from 'react';

// Define all required types
export interface MarketData {
  volume_24h: number;
  market_cap: number;
  percent_change_24h: number;
  percent_change_7d: number;
}

export interface Prediction {
  id: number;  // Changed from string to number to match existing type
  asset: string;
  currentPrice: number;
  predictedPrice: number;
  confidence: number;
  reasoning: string;
  marketData?: MarketData;
  // Binary market specific fields
  question?: string;
  endTimestamp?: number;
  yesPrice?: number;
  noPrice?: number;
  totalLiquidity?: number;
  predictorType: 'AI' | 'KOL';
}

interface Props {
  prediction: Prediction;
  isAI: boolean;
}

const formatPrice = (price: number) => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(price);
};

const formatPercent = (value: number) => {
  return `${value > 0 ? '+' : ''}${value.toFixed(1)}%`;
};

const PredictionCard: React.FC<Props> = ({ prediction, isAI }) => {
  const [selectedOutcome, setSelectedOutcome] = useState<'YES' | 'NO' | null>(null);
  const [amount, setAmount] = useState("");
  const [isProcessing, setIsProcessing] = useState(false);

  const priceChange = prediction.predictedPrice - prediction.currentPrice;
  const priceChangePercent = (priceChange / prediction.currentPrice) * 100;

  const calculatePayout = (outcome: 'YES' | 'NO', betAmount: number) => {
    if (!prediction.yesPrice || !prediction.noPrice) return 0;
    const price = outcome === 'YES' ? prediction.yesPrice : prediction.noPrice;
    return betAmount / price;
  };

  const handleBet = async () => {
    if (!selectedOutcome || !amount) return;
    
    setIsProcessing(true);
    try {
      const betAmount = parseFloat(amount);
      const payout = calculatePayout(selectedOutcome, betAmount);
      
      // TODO: Add API call to place bet
      console.log(`Placing ${selectedOutcome} bet:`, {
        amount: betAmount,
        payout,
        market: prediction.asset
      });
      
    } catch (error) {
      console.error('Error placing bet:', error);
    } finally {
      setIsProcessing(false);
    }
  };

  // Check if this is a binary market
  const isBinaryMarket = Boolean(prediction.question && prediction.yesPrice && prediction.noPrice);

  // Safe getters for optional values
  const getYesPrice = () => (prediction.yesPrice ?? 0) * 100;
  const getNoPrice = () => (prediction.noPrice ?? 0) * 100;
  const getTotalLiquidity = () => prediction.totalLiquidity ?? 0;
  const getTimeRemaining = () => {
    if (!prediction.endTimestamp) return 0;
    return Math.max(0, Math.floor((prediction.endTimestamp - Date.now()) / (1000 * 60 * 60 * 24)));
  };

  return (
    <div className="border rounded-lg p-4 bg-white shadow-md mb-4">
      {/* Header */}
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-semibold">
          {isBinaryMarket ? prediction.question : `${prediction.asset}/USD`}
        </h3>
        <span className="text-sm text-gray-500">
          {isAI ? 'AI Prediction' : 'KOL Prediction'}
        </span>
      </div>

      {isBinaryMarket ? (
        // Binary Market View
        <>
          {/* Market Prices */}
          <div className="grid grid-cols-2 gap-4 mb-6">
            <div className="p-4 border rounded-lg">
              <p className="text-lg font-semibold text-green-600">YES</p>
              <p className="text-2xl font-bold">
                {formatPercent(getYesPrice())}
              </p>
            </div>
            <div className="p-4 border rounded-lg">
              <p className="text-lg font-semibold text-red-600">NO</p>
              <p className="text-2xl font-bold">
                {formatPercent(getNoPrice())}
              </p>
            </div>
          </div>

          {/* Market Info */}
          <div className="grid grid-cols-2 gap-4 mb-6 text-sm">
            <div>
              <p className="text-gray-600">Total Liquidity</p>
              <p className="font-medium">{formatPrice(getTotalLiquidity())}</p>
            </div>
            <div>
              <p className="text-gray-600">Time Remaining</p>
              <p className="font-medium">{getTimeRemaining()} days</p>
            </div>
          </div>

          {/* Betting Interface */}
          <div className="mt-6 p-4 border rounded-lg">
            <div className="flex gap-4 mb-4">
              <button
                onClick={() => setSelectedOutcome('YES')}
                className={`flex-1 py-2 rounded-lg ${
                  selectedOutcome === 'YES'
                    ? 'bg-green-600 text-white'
                    : 'bg-gray-100 hover:bg-gray-200'
                }`}
              >
                YES
              </button>
              <button
                onClick={() => setSelectedOutcome('NO')}
                className={`flex-1 py-2 rounded-lg ${
                  selectedOutcome === 'NO'
                    ? 'bg-red-600 text-white'
                    : 'bg-gray-100 hover:bg-gray-200'
                }`}
              >
                NO
              </button>
            </div>

            <div className="flex gap-2">
              <input
                type="number"
                className="flex-1 border rounded px-3 py-2"
                placeholder="Enter amount"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
              />
              <button
                onClick={handleBet}
                disabled={isProcessing || !selectedOutcome || !amount}
                className={`px-4 py-2 rounded text-white ${
                  isProcessing || !selectedOutcome || !amount
                    ? 'bg-gray-400'
                    : 'bg-blue-500 hover:bg-blue-600'
                }`}
              >
                Place Bet
              </button>
            </div>

            {selectedOutcome && amount && (
              <div className="mt-4 text-sm">
                <p>Potential Payout: {formatPrice(calculatePayout(selectedOutcome, parseFloat(amount)))}</p>
              </div>
            )}
          </div>
        </>
      ) : (
        // Price Prediction View
        <>
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
        </>
      )}
    </div>
  );
};

export default PredictionCard;