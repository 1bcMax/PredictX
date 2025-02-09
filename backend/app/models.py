from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MarketData(BaseModel):
    volume_24h: float
    market_cap: float
    percent_change_24h: float
    percent_change_7d: float

class Prediction(BaseModel):
    id: int
    asset: str
    currentPrice: float
    predictedPrice: float
    confidence: float
    reasoning: str
    predictorType: str
    marketData: Optional[MarketData] = None
    
    # Binary market specific fields
    question: Optional[str] = None
    endTimestamp: Optional[float] = None
    yesPrice: Optional[float] = None
    noPrice: Optional[float] = None
    totalLiquidity: Optional[float] = None