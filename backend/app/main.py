from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from app.services.prediction_service import PredictionService
from app.services.agent_service import AgentService
from dotenv import load_dotenv
import logging

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
agent_service = AgentService()  # Agent is initialized on startup
prediction_service = PredictionService(agent_service)

@app.get("/predictions")
async def get_predictions():
    try:
        return await prediction_service.get_all_predictions()
    except Exception as e:
        logger.error(f"Error getting predictions: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predictions/ai")
async def create_ai_prediction(request: Request): # Change to Request type
    try:
        body = await request.json() # Get body explicitly
        asset = body.get("asset")
        if not asset:
            raise HTTPException(status_code=400, detail="Asset is required")
        return await prediction_service.create_ai_prediction(asset)
    except Exception as e:
        logger.error(f"Error creating AI prediction: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/support")
async def support_prediction(request: Request): # Change to Request Type
    try:
        body = await request.json()
        prediction_id = body.get("predictionId")
        amount = body.get("amount")
        support_ai = body.get("supportAi")

        if prediction_id is None or amount is None or support_ai is None:
            raise HTTPException(status_code=400, detail="Missing required parameters")

        return await prediction_service.support_prediction(prediction_id, amount, support_ai)
    except Exception as e:
        logger.error(f"Error supporting prediction: {e}")
        raise HTTPException(status_code=500, detail=str(e))