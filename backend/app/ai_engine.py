from openai import AzureOpenAI
from .price_service import PriceService
import os
from dotenv import load_dotenv
import json
import logging

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIPredictionEngine:
    def __init__(self):
        self.client = AzureOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION")
        )
        self.deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
        self.price_service = PriceService()

    async def generate_prediction(self, asset: str) -> dict:
        try:
            # 获取市场数据
            market_data = await self.price_service.get_market_data(asset)
            current_price = market_data['current_price']
            
            # 构建包含市场数据的提示
            prompt = [
                {
                    "role": "system",
                    "content": """You are a professional crypto trader AI. 
                    Analyze the provided market data and generate a price prediction.
                    Consider recent price changes, volume, and market cap.
                    Be specific and quantitative in your analysis.
                    Format your response as JSON with fields: predictedPrice, confidence, reasoning."""
                },
                {
                    "role": "user",
                    "content": f"""Generate a 24-hour price prediction for {asset} based on this market data:
                    Current Price: ${current_price:.2f}
                    24h Change: {market_data['percent_change_24h']}%
                    7d Change: {market_data['percent_change_7d']}%
                    24h Volume: ${market_data['volume_24h']:,.2f}
                    Market Cap: ${market_data['market_cap']:,.2f}"""
                }
            ]

            completion = self.client.chat.completions.create(
                model=self.deployment,
                messages=prompt,
                max_tokens=800,
                temperature=0.7,
                top_p=0.95
            )

            # Parse the response as JSON
            response_text = completion.choices[0].message.content
            prediction_data = json.loads(response_text)
            
            # 添加当前价格和市场数据
            prediction_data.update({
                "asset": asset,
                "predictorType": "AI",
                "currentPrice": current_price,
                "marketData": market_data
            })

            logger.info(f"Generated prediction for {asset}: {prediction_data}")
            return prediction_data

        except Exception as e:
            logger.error(f"Error generating prediction: {e}")
            # Fallback prediction using current price
            current_price = await self.price_service.get_price(asset)
            return {
                "asset": asset,
                "predictorType": "AI",
                "currentPrice": current_price,
                "predictedPrice": current_price * 1.05,  # 假设5%的增长
                "confidence": 0.6,
                "reasoning": "Fallback prediction based on current market price."
            }