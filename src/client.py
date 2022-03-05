from pprint import pprint
from datetime import datetime, timedelta

import alpaca_trade_api as trade_api
from src.config import get_key


api_client = trade_api.REST(
	key_id=get_key("ALPACA_KEY_ID"),
	secret_key=get_key("ALPACA_SECRET_KEY"),
	base_url=get_key("ALPACA_BASE_URL"),
)

class Client():
	def __init__(self):
		self.api_client = api_client
		pprint(self.api_client)

if __name__ == "__main__":
	c = Client()