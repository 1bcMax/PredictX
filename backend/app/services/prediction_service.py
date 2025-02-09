from app.services.agent_service import AgentService
from app.models.prediction import Prediction
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class PredictionService:
    def __init__(self, agent_service: AgentService):
        self.agent_service = agent_service
        self.predictions = []  # Replace with database later

    async def get_all_predictions(self) -> list:
        """Get all predictions."""
        return self.predictions

    async def create_ai_prediction(self, asset: str) -> dict:
        """Create a new AI prediction."""
        try:
            # Generate prediction using AgentKit
            prediction_data = await self.agent_service.generate_prediction(asset)

            # Create prediction record
            prediction = Prediction(
                asset=asset,
                current_price=prediction_data.get("currentPrice"),  # Use .get() for safety
                predicted_price=prediction_data.get("predictedPrice"),
                confidence=prediction_data.get("confidence"),
                prediction_time=datetime.utcnow(),
                is_ai=True,
                reasoning=prediction_data.get("reasoning")
            )

            self.predictions.append(prediction)
            # Return a dictionary representation of the Prediction object
            return prediction.model_dump() # Use model_dump() instead of dict()

        except Exception as e:
            logger.error(f"Error creating prediction: {e}")
            raise


    async def support_prediction(self, prediction_id: int, amount: float, support_ai: bool) -> dict:
        """Support or oppose a prediction."""
        # Placeholder for future CDP AgentKit integration for on-chain actions.
        # This is where you'd interact with the blockchain, likely using
        # custom tools within the AgentKit.
        logger.info(
            f"Support/oppose called for prediction ID {prediction_id} with amount {amount}. "
            f"Supporting AI: {support_ai}"
        )
        return {"status": "success", "message": "Support/oppose action recorded (placeholder)."}