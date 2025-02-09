from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging
from typing import List
from .ai_engine import AIPredictionEngine
from .models import Prediction

app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize AI engine
ai_engine = AIPredictionEngine()

# In-memory storage for predictions (replace with database in production)
predictions: List[Prediction] = []

@app.get("/predictions")
async def get_predictions():
    return predictions

@app.post("/predictions/ai")
async def create_ai_prediction(asset: str = "BTC"):
    try:
        # First try to generate a binary market prediction
        prediction = await ai_engine.generate_binary_market(
            asset=asset,
            target_price=None,  # It will calculate based on current price
            duration_days=1
        )
        
        # Convert to your Prediction model format
        new_prediction = Prediction(
            id=len(predictions) + 1,
            asset=prediction["asset"],
            currentPrice=prediction["currentPrice"],
            predictedPrice=prediction["targetPrice"],
            confidence=prediction["confidence"],
            reasoning=prediction["reasoning"],
            predictorType="AI",
            # Binary market specific fields
            question=prediction["question"],
            endTimestamp=prediction["endTimestamp"],
            yesPrice=prediction["yesPrice"],
            noPrice=prediction["noPrice"],
            totalLiquidity=prediction["totalLiquidity"],
            marketData=prediction.get("marketData")
        )
        
        predictions.append(new_prediction)
        return new_prediction
        
    except Exception as e:
        logger.error(f"Error creating AI prediction: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Add other endpoints as needed...