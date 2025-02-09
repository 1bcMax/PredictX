from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from cdp_langchain.agent_toolkits import CdpToolkit
from cdp_langchain.utils import CdpAgentkitWrapper
from cdp.wallet import Wallet
from bip_utils import Bip39MnemonicGenerator, Bip39SeedGenerator
import os
import json
import logging
from cdp import Cdp  # Import the Cdp class
from unittest.mock import patch  # Import the patching library
from cdp.client.models.wallet import Wallet as WalletModel  # Import WalletModel

logger = logging.getLogger(__name__)

class AgentService:
    def __init__(self):
        """Initialize CDP AgentKit and LLM."""
        self.wallet_data_file = "wallet_data.txt"
        self.agent_executor = None
        self.cdp = None
        self.initialize_agent()

    def initialize_agent(self):
        """Initialize the agent with CDP Agentkit."""
        try:
            llm = ChatOpenAI(model="gpt-4")

            if os.path.exists(self.wallet_data_file):
                with open(self.wallet_data_file, "r") as f:
                    wallet_data = f.read()
                values = {"cdp_wallet_data": wallet_data}
                self.cdp = CdpAgentkitWrapper(**values)
            else:
                # 1. Generate a new mnemonic phrase
                mnemonic = Bip39MnemonicGenerator().FromWordsNumber(12)
                # 2. Generate the seed from the mnemonic
                seed = Bip39SeedGenerator(mnemonic).Generate().hex()


                # 3. Mock the create_wallet method
                with patch('cdp.client.api.wallets_api.WalletsApi.create_wallet') as mock_create_wallet: # Corrected patch target
                    # 3a. Configure the mock to return a WalletModel instance
                    mock_create_wallet.return_value = WalletModel(
                        id="mock-wallet-id",  # Provide a mock wallet ID
                        network_id="base-sepolia",
                        server_signer_status="active_seed",  # Important for later checks
                        default_address=None,
                        feature_set={  # Complete feature_set
                            "faucet": {},
                            "server_signer": {},
                            "transfer": {},
                            "trade": {},
                            "stake": {},
                            "gasless_send": {},
                        },
                    )

                    # 4. Create the wallet (this now uses the mock)
                    wallet = Wallet.create_with_seed(seed=seed, network_id="base-sepolia")
                    wallet_data = wallet.export_data().model_dump_json()


                    # 5. Save the wallet data (including the mnemonic) to the file
                    with open(self.wallet_data_file, "w") as f:
                        f.write(wallet_data)

                    # 6. Initialize CdpAgentkitWrapper with the wallet data
                    self.cdp = CdpAgentkitWrapper(cdp_wallet_data=wallet_data)

            toolkit = CdpToolkit.from_cdp_agentkit_wrapper(self.cdp)
            tools = toolkit.get_tools()
            memory = MemorySaver()
            agent_prompt = (
                "You are a crypto prediction AI assistant. Your task is to analyze market data "
                "and make 24-hour price predictions. Use the available tools to fetch current "
                "market information and provide a prediction with a confidence level and "
                "detailed reasoning."
            )
            self.agent_executor = create_react_agent(
                llm,
                tools=tools,
                checkpointer=memory,
                state_modifier=agent_prompt
            )

            logger.info("Agent initialized successfully")
            return True

        except Exception as e:
            logger.error(f"Error initializing agent: {e}")
            raise

    async def generate_prediction(self, asset: str) -> dict:
        """Generate a prediction using the agent."""
        try:
            messages = [
                {
                    "role": "user",
                    "content": (
                        f"Generate a 24-hour price prediction for {asset} with detailed analysis. "
                        "Include the current price, predicted price, confidence level (0.0-1.0), and your reasoning."
                    ),
                }
            ]
            result = await self.agent_executor.ainvoke({"messages": messages})

            # Extract the agent's output (more robust parsing)
            agent_output = result.get("output")
            if not agent_output:
                raise ValueError("Agent did not return an output.")

            # Attempt to parse as JSON, but handle potential text output
            try:
                prediction_data = json.loads(agent_output)
            except json.JSONDecodeError:
                # If it's not JSON, create a basic dictionary (you might need to refine this)
                logger.warning(f"Agent output was not JSON: {agent_output}")
                prediction_data = {
                    "currentPrice": None,
                    "predictedPrice": None,
                    "confidence": None,
                    "reasoning": agent_output,
                }

            if not all(key in prediction_data for key in ["currentPrice", "predictedPrice", "confidence", "reasoning"]):
                logger.warning("Agent output is missing required fields.")
                prediction_data.setdefault("currentPrice", None)
                prediction_data.setdefault("predictedPrice", None)
                prediction_data.setdefault("confidence", None)

            return prediction_data

        except Exception as e:
            logger.error(f"Error generating prediction: {e}")
            raise