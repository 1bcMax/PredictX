from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal
from typing import Optional

class Prediction(BaseModel):
    id: Optional[int]
    predictor_type: str  # 'AI' or 'KOL'
    predictor_id: str
    asset: str
    predicted_price: Decimal
    prediction_time: datetime
    confidence: float
    reasoning: str

class Stake(BaseModel):
    prediction_id: int
    user_address: str
    amount: Decimal
    support_ai: bool
