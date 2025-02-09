from openai import AzureOpenAI
from .price_service import PriceService
import os
from dotenv import load_dotenv
import json
import logging
from datetime import datetime, timedelta

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

    async def generate_binary_market(self, asset: str, target_price: float = None, duration_days: int = 1) -> dict:
        """
        Generates a binary market prediction for whether an asset will reach a target price
        """
        try:
            # Get market data
            market_data = await self.price_service.get_market_data(asset)
            current_price = market_data['current_price']
            
            # If target_price is None, set it to a default value (e.g., 5% above current price)
            if target_price is None:
                target_price = current_price * 1.05  # 5% above current price
            
            # Calculate price difference percentage
            price_difference_percent = ((target_price - current_price) / current_price) * 100
            
            # Build prompt for binary prediction
            prompt = [
                {
                    "role": "system",
                    "content": """You are a professional crypto trading AI analyzing market conditions.
                    Based on the provided market data, estimate the probability of the asset reaching
                    the target price within the specified timeframe. Consider market momentum,
                    volume, and historical volatility.
                    Format your response as JSON with fields:
                    - yesProbability: float between 0 and 1
                    - noProbability: float between 0 and 1 (must sum to 1 with yesProbability)
                    - confidence: float between 0 and 1
                    - reasoning: string explaining the prediction"""
                },
                {
                    "role": "user",
                    "content": f"""Analyze the probability of {asset} reaching ${target_price:,.2f} 
                    (a {price_difference_percent:,.1f}% change) within {duration_days} days.
                    
                    Current market data:
                    Current Price: ${current_price:,.2f}
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

            # Parse the AI response
            response_text = completion.choices[0].message.content
            prediction_data = json.loads(response_text)
            
            # Calculate end timestamp
            end_timestamp = datetime.now() + timedelta(days=duration_days)
            
            # Create market structure
            market = {
                "asset": asset,
                "predictorType": "AI",
                "question": f"Will {asset} reach ${target_price:,.2f} by {end_timestamp.strftime('%Y-%m-%d')}?",
                "currentPrice": current_price,
                "targetPrice": target_price,
                "endTimestamp": end_timestamp.timestamp(),
                "yesPrice": prediction_data["yesProbability"],
                "noPrice": prediction_data["noProbability"],
                "confidence": prediction_data["confidence"],
                "reasoning": prediction_data["reasoning"],
                "marketData": market_data,
                "totalLiquidity": 1000.0,  # Initial liquidity pool
                "yesLiquidity": 1000.0 * prediction_data["yesProbability"],
                "noLiquidity": 1000.0 * prediction_data["noProbability"]
            }

            logger.info(f"Generated binary market for {asset}: {market}")
            return market

        except Exception as e:
            logger.error(f"Error generating binary market: {e}")
            # Fallback prediction
            end_timestamp = datetime.now() + timedelta(days=duration_days)
            return {
                "asset": asset,
                "predictorType": "AI",
                "question": f"Will {asset} reach ${target_price:,.2f} by {end_timestamp.strftime('%Y-%m-%d')}?",
                "currentPrice": current_price,
                "targetPrice": target_price,
                "endTimestamp": end_timestamp.timestamp(),
                "yesPrice": 0.5,
                "noPrice": 0.5,
                "confidence": 0.6,
                "reasoning": "Fallback prediction due to error. Using neutral 50-50 probability.",
                "marketData": market_data,
                "totalLiquidity": 1000.0,
                "yesLiquidity": 500.0,
                "noLiquidity": 500.0
            }

    async def generate_price_prediction(self, asset: str) -> dict:
        """
        Original price prediction method (maintained for backwards compatibility)
        """
        try:
            # Get market data
            market_data = await self.price_service.get_market_data(asset)
            current_price = market_data['current_price']
            
            # Build prompt
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
            
            # Add current price and market data
            prediction_data.update({
                "asset": asset,
                "predictorType": "AI",
                "currentPrice": current_price,
                "marketData": market_data
            })

            logger.info(f"Generated price prediction for {asset}: {prediction_data}")
            return prediction_data

        except Exception as e:
            logger.error(f"Error generating prediction: {e}")
            # Fallback prediction using current price
            current_price = await self.price_service.get_price(asset)
            return {
                "asset": asset,
                "predictorType": "AI",
                "currentPrice": current_price,
                "predictedPrice": current_price * 1.05,  # Assume 5% growth
                "confidence": 0.6,
                "reasoning": "Fallback prediction based on current market price."
            }