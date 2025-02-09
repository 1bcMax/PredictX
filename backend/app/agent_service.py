import os
import logging
from dotenv import load_dotenv
from solcx import compile_standard, install_solc
from typing import Optional
from cdp_langchain.agent_toolkits import CdpToolkit
from cdp_langchain.utils import CdpAgentkitWrapper
from cdp import Wallet  # Import for type hinting and place_bet


load_dotenv()
logger = logging.getLogger(__name__)


class AgentService:
    def __init__(self):
        try:
            # Get API key and private key from environment variables
            api_key_name = os.getenv('CDP_API_KEY_NAME')
            api_key_private_key = os.getenv('CDP_API_KEY_PRIVATE_KEY')
            network_id = "base-sepolia"  # Or get from .env if you prefer

            if not api_key_name or not api_key_private_key:
                raise ValueError("CDP_API_KEY_NAME and CDP_API_KEY_PRIVATE_KEY must be set in .env")

            # Pass API key and private key *directly* to CdpAgentkitWrapper
            self.agentkit = CdpAgentkitWrapper(
                api_key_name=api_key_name,
                api_key_private_key=api_key_private_key,
                network_id=network_id  # Good practice to include
            )
            self.wallet_data = self.agentkit.export_wallet()  # Get wallet data
            logger.info(f"Wallet Data: {self.wallet_data}")

            # Initialize CDP Agentkit Toolkit.
            cdp_toolkit = CdpToolkit.from_cdp_agentkit_wrapper(self.agentkit)
            self.tools = cdp_toolkit.get_tools()  # Get the tools, though we don't use them directly here

            # We can access the underlying wallet through the agentkit.
            self.wallet = self.agentkit.wallet
            self.address = self.wallet.default_address
            self.private_key = self.wallet.private_key  # access private key
            logger.info(f"Deployment Wallet Address: {self.address}")

            # Try to fund the wallet
            try:
                faucet_tx = self.wallet.faucet()
                faucet_tx.wait()
                logger.info(f"Faucet transaction successful: {faucet_tx}")
            except Exception as e:
                logger.error(f"Faucet transaction failed: {e}")

            # Set chain constants
            self.usdc_address = "0x50c5725949A6F0c72E6C4a641F24049A917DB0Cb"
            self.base_chain_id = 84532

        except Exception as e:
            logger.error(f"Error initializing AgentService: {e}")
            raise ValueError(f"Failed to initialize AgentService: {str(e)}")

    def _compile_solidity(self, solidity_code: str, contract_name: str):
        """Compiles Solidity code using py-solc-x."""
        try:
            install_solc('0.8.20')
            compiled_sol = compile_standard(
                {
                    "language": "Solidity",
                    "sources": {f"{contract_name}.sol": {"content": solidity_code}},
                    "settings": {
                        "outputSelection": {"*": {"*": ["abi", "evm.bytecode"]}}
                    },
                },
                solc_version="0.8.20",
            )
            return compiled_sol
        except Exception as e:
            logger.error(f"Solidity compilation error: {e}")
            raise

    async def create_market(self, market_data: dict) -> Optional[str]:
        """Creates a market by deploying a smart contract."""
        try:
            # Get the contract code and compile it
            solidity_code = self._get_prediction_market_contract()
            contract_name = "PredictionMarket"
            compiled_sol = self._compile_solidity(solidity_code, contract_name)

            if not compiled_sol:
                return None

            # Get contract interface
            contract_interface = compiled_sol["contracts"][f"{contract_name}.sol"][contract_name]
            abi = contract_interface["abi"]
            bytecode = contract_interface["evm"]["bytecode"]["object"]

            # Convert prices to the correct decimal format
            yes_price_decimal = int(market_data["yesPrice"] * (10**18))
            no_price_decimal = int(market_data["noPrice"] * (10**18))

            # Deploy the contract using the agentkit's wallet
            contract = self.wallet.deploy_contract(
                abi=abi,
                bytecode=bytecode,
                constructor_args=[
                    market_data["question"],
                    int(market_data["endTimestamp"]),
                    self.usdc_address,
                    yes_price_decimal,
                    no_price_decimal
                ],
            ).wait()

            logger.info(f"Deployed market contract at: {contract.contract_address}")
            return contract.contract_address

        except Exception as e:
            logger.error(f"Error creating market: {e}")
            return None
    async def place_bet(self, market_address: str, outcome: str, amount: float, user_wallet: Wallet) -> bool:
        """Places a bet (buyYes or buyNo)."""
        try:
            solidity_code = self._get_prediction_market_contract()
            contract_name = "PredictionMarket"
            compiled_sol = self._compile_solidity(solidity_code, contract_name)
            contract_interface = compiled_sol["contracts"][f"{contract_name}.sol"][contract_name]
            abi = contract_interface["abi"]

            # Load contracts
            contract = user_wallet.load_contract(address=market_address, abi=abi) # use user wallet
            amount_decimal = int(amount * (10**6))  # USDC has 6 decimals

            # Approve USDC transfer
            usdc_contract = user_wallet.load_contract(address=self.usdc_address, abi=[
                {"name": "approve", "inputs": [{"type": "address", "name": "spender"}, {"type": "uint256", "name": "amount"}], "outputs": [{"type": "bool"}], "type": "function"},
                {"name": "balanceOf", "inputs": [{"type": "address", "name": "account"}], "outputs": [{"type": "uint256"}], "type": "function"},
            ])

            # Check balance and approve
            current_balance = usdc_contract.functions.balanceOf(user_wallet.address).call()
            logger.info(f"Current USDC balance: {current_balance}")

            approval_tx = usdc_contract.functions.approve(market_address, amount_decimal).transact(chain_id=self.base_chain_id)
            approval_receipt = user_wallet.w3.eth.wait_for_transaction_receipt(approval_tx)
            logger.info(f"USDC approval transaction: {approval_receipt}")

            # Place bet
            if outcome.lower() == "yes":
                tx_hash = contract.functions.buyYes(amount_decimal).transact(chain_id=self.base_chain_id)
            elif outcome.lower() == "no":
                tx_hash = contract.functions.buyNo(amount_decimal).transact(chain_id=self.base_chain_id)
            else:
                raise ValueError("Invalid outcome")

            receipt = user_wallet.w3.eth.wait_for_transaction_receipt(tx_hash)
            logger.info(f"{outcome.capitalize()} purchase transaction receipt: {receipt}")
            return True

        except Exception as e:
            logger.error(f"Error placing bet: {e}")
            return False

    async def resolve_market(self, market_address: str, winning_outcome: str) -> bool:
        """Resolves a market."""
        try:
            solidity_code = self._get_prediction_market_contract()
            contract_name = "PredictionMarket"
            compiled_sol = self._compile_solidity(solidity_code, contract_name)
            contract_interface = compiled_sol["contracts"][f"{contract_name}.sol"][contract_name]
            abi = contract_interface["abi"]

            contract = self.wallet.load_contract(address=market_address, abi=abi) # use agentkit wallet
            outcome_bool = winning_outcome.lower() == "yes"
            tx_hash = contract.functions.resolve(outcome_bool).transact(chain_id=self.base_chain_id)
            receipt = self.wallet.w3.eth.wait_for_transaction_receipt(tx_hash)
            logger.info(f"Resolve transaction receipt: {receipt}")
            return True

        except Exception as e:
            logger.error(f"Error resolving market: {e}")
            return False
    async def get_market_details(self, market_address: str):
        """Gets market details."""
        try:
            solidity_code = self._get_prediction_market_contract()
            contract_name = "PredictionMarket"
            compiled_sol = self._compile_solidity(solidity_code, contract_name)
            contract_interface = compiled_sol["contracts"][f"{contract_name}.sol"][contract_name]
            abi = contract_interface["abi"]

            contract = self.wallet.load_contract(address=market_address, abi=abi) # use agentkit wallet

            # Get contract details
            question = contract.functions.question().call()
            endTime = contract.functions.endTime().call()
            resolved = contract.functions.resolved().call()
            yesPrice = contract.functions.yesPrice().call() / (10**18)
            noPrice = contract.functions.noPrice().call() / (10**18)
            creator = contract.functions.creator().call()

            details = {
                "question": question,
                "endTime": endTime,
                "resolved": resolved,
                "yesPrice": yesPrice,
                "noPrice": noPrice,
                "creator": creator
            }

            logger.info(f"Market details: {details}")
            return details

        except Exception as e:
            logger.error(f"Error getting market details: {e}")
            return None

    async def get_user_balance(self, market_address: str, user_address: str):
        """Gets user yes/no balance."""
        try:
            solidity_code = self._get_prediction_market_contract()
            contract_name = "PredictionMarket"
            compiled_sol = self._compile_solidity(solidity_code, contract_name)
            contract_interface = compiled_sol["contracts"][f"{contract_name}.sol"][contract_name]
            abi = contract_interface["abi"]

            contract = self.wallet.load_contract(address=market_address, abi=abi) # use agentkit wallet
            yes_balance, no_balance = contract.functions.getBalance(user_address).call()

            return {
                "yesBalance": yes_balance,
                "noBalance": no_balance,
            }

        except Exception as e:
            logger.error(f"Error getting user balance: {e}")
            return None
    def _get_prediction_market_contract(self) -> str:
        """Returns the Solidity code for the prediction market contract."""
        return """
        // SPDX-License-Identifier: MIT
        pragma solidity ^0.8.20;
        contract PredictionMarket {
            string public question;
            uint256 public endTime;
            address public creator;
            address public usdcToken;
            bool public resolved;
            bool public outcome;
            uint256 public yesPrice;
            uint256 public noPrice;
            mapping(address => uint256) public yesBalances;
            mapping(address => uint256) public noBalances;

            constructor(string memory _question, uint256 _endTime, address _usdcToken, uint256 _yesPrice, uint256 _noPrice) {
                question = _question;
                endTime = _endTime;
                creator = msg.sender;
                usdcToken = _usdcToken;
                yesPrice = _yesPrice;
                noPrice = _noPrice;
                resolved = false;
            }

            function buyYes(uint256 amount) public {
                require(block.timestamp < endTime, "Market has ended.");
                require(!resolved, "Market has been resolved.");
                uint256 cost = amount * yesPrice;
                IERC20(usdcToken).transferFrom(msg.sender, address(this), cost);
                yesBalances[msg.sender] += amount;
            }

            function buyNo(uint256 amount) public {
                require(block.timestamp < endTime, "Market has ended.");
                require(!resolved, "Market has been resolved.");
                uint256 cost = amount * noPrice;
                IERC20(usdcToken).transferFrom(msg.sender, address(this), cost);
                noBalances[msg.sender] += amount;
            }

            function resolve(bool _outcome) public {
                require(msg.sender == creator, "Only creator can resolve.");
                require(block.timestamp >= endTime, "Market has not ended.");
                require(!resolved, "Market has already been resolved.");
                resolved = true;
                outcome = _outcome;
            }

            function getBalance(address user) public view returns (uint256 yes, uint256 no) {
                return (yesBalances[user], noBalances[user]);
            }
        }

        interface IERC20 {
            function transferFrom(address sender, address recipient, uint256 amount) external returns (bool);
            function transfer(address recipient, uint256 amount) external returns (bool);
            function balanceOf(address account) external view returns (uint256);
            function approve(address spender, uint256 amount) external returns (bool);
        }
        """