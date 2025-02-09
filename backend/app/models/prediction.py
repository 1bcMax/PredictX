from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Prediction(BaseModel):
    id: Optional[int] = None  #  Consider auto-incrementing in the database
    asset: str
    current_price: float
    predicted_price: float
    confidence: float
    prediction_time: datetime
    is_ai: bool
    reasoning: str