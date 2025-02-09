import os
import requests
from dotenv import load_dotenv
import logging

load_dotenv()
logger = logging.getLogger(__name__)

class PriceService:
    def __init__(self):
        self.api_key = os.getenv("COINMARKETCAP_API_KEY")
        self.base_url = "https://pro-api.coinmarketcap.com/v1"
        
        if not self.api_key:
            raise ValueError("COINMARKETCAP_API_KEY not found in environment variables")

    async def get_price(self, symbol: str) -> float:
        """
        Get current price for a cryptocurrency
        :param symbol: Cryptocurrency symbol (e.g., 'BTC', 'ETH')
        :return: Current price in USD
        """
        try:
            headers = {
                'X-CMC_PRO_API_KEY': self.api_key,
                'Accept': 'application/json'
            }
            
            # Convert common symbols to CMC format
            symbol = symbol.upper()
            
            params = {
                'symbol': symbol,
                'convert': 'USD'
            }
            
            response = requests.get(
                f"{self.base_url}/cryptocurrency/quotes/latest",
                headers=headers,
                params=params
            )
            
            response.raise_for_status()
            data = response.json()
            
            if not data['data'] or symbol not in data['data']:
                raise ValueError(f"Price not found for {symbol}")
                
            price = data['data'][symbol]['quote']['USD']['price']
            logger.info(f"Got price for {symbol}: ${price}")
            return price
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching price from CoinMarketCap: {e}")
            raise
            
    async def get_market_data(self, symbol: str) -> dict:
        """
        Get detailed market data for a cryptocurrency
        :param symbol: Cryptocurrency symbol (e.g., 'BTC', 'ETH')
        :return: Dictionary with market data
        """
        try:
            headers = {
                'X-CMC_PRO_API_KEY': self.api_key,
                'Accept': 'application/json'
            }
            
            symbol = symbol.upper()
            params = {
                'symbol': symbol,
                'convert': 'USD'
            }
            
            response = requests.get(
                f"{self.base_url}/cryptocurrency/quotes/latest",
                headers=headers,
                params=params
            )
            
            response.raise_for_status()
            data = response.json()['data'][symbol]
            quote = data['quote']['USD']
            
            return {
                'current_price': quote['price'],
                'market_cap': quote['market_cap'],
                'volume_24h': quote['volume_24h'],
                'percent_change_1h': quote['percent_change_1h'],
                'percent_change_24h': quote['percent_change_24h'],
                'percent_change_7d': quote['percent_change_7d']
            }
            
        except Exception as e:
            logger.error(f"Error fetching market data for {symbol}: {e}")
            raise