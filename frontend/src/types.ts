export interface MarketData {
  current_price: number;
  market_cap: number;
  volume_24h: number;
  percent_change_1h: number;
  percent_change_24h: number;
  percent_change_7d: number;
}

export interface Prediction {
  id: number;
  predictorType: 'AI' | 'KOL';
  asset: string;
  currentPrice: number;
  predictedPrice: number;
  confidence: number;
  reasoning: string;
  marketData?: MarketData;
  supportersCount?: number;
  totalSupport?: number;
}

export interface Stake {
  predictionId: number;
  userAddress: string;
  amount: number;
  supportAi: boolean;
}