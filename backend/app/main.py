from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List
from pydantic import BaseModel
from .ai_engine import AIPredictionEngine
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AssetRequest(BaseModel):
    asset: str

class SupportRequest(BaseModel):
    predictionId: int
    amount: float
    supportAi: bool

app = FastAPI()

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化 AI 引擎
ai_engine = AIPredictionEngine()

# 存储数据
predictions: List[Dict] = []
supports: List[Dict] = []
prediction_id_counter = 1

@app.get("/predictions")
async def get_predictions():
    enriched_predictions = []
    for pred in predictions:
        pred_supports = [s for s in supports if s["predictionId"] == pred["id"]]
        total_amount = sum(s["amount"] for s in pred_supports)
        supporters_count = len(pred_supports)
        
        enriched_pred = {
            **pred,
            "totalSupport": total_amount,
            "supportersCount": supporters_count
        }
        enriched_predictions.append(enriched_pred)
    
    return enriched_predictions

@app.post("/predictions/ai")
async def create_ai_prediction(request: AssetRequest):
    try:
        global prediction_id_counter
        # 使用 AI 引擎生成预测
        prediction_data = await ai_engine.generate_prediction(request.asset)
        
        # 添加 ID 和其他必要字段
        prediction = {
            "id": prediction_id_counter,
            **prediction_data,
            "supportersCount": 0,
            "totalSupport": 0
        }
        prediction_id_counter += 1
        predictions.append(prediction)
        
        logger.info(f"Created new AI prediction: {prediction}")
        return prediction
    except Exception as e:
        logger.error(f"Error creating AI prediction: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predictions/kol")
async def create_kol_prediction(prediction: Dict):
    global prediction_id_counter
    prediction["id"] = prediction_id_counter
    prediction["supportersCount"] = 0
    prediction["totalSupport"] = 0
    prediction_id_counter += 1
    predictions.append(prediction)
    return prediction

@app.post("/support")
async def support_prediction(support: SupportRequest):
    prediction = next(
        (p for p in predictions if p["id"] == support.predictionId),
        None
    )
    
    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction not found")
        
    support_data = {
        "predictionId": support.predictionId,
        "amount": support.amount,
        "supportAi": support.supportAi
    }
    supports.append(support_data)
    
    logger.info(f"New support added: {support_data}")
    return {
        "status": "success",
        "support": support_data
    }