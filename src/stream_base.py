from pathlib import Path
import json
from datetime import datetime, timezone

from src.config import get_key
from src.candle.candle import Candle
from alpaca_trade_api.stream import Stream

dir = Path(__file__).parent.resolve()

class BaseStreamer:
	def __init__(self, symbol: str):
		self.stream = Stream(
			key_id=get_key("ALPACA_KEY_ID"),
			secret_key=get_key("ALPACA_SECRET_KEY"),
			base_url=get_key("ALPACA_BASE_URL"),
			data_feed="iex", 
			raw_data=False,
		)

		self.exchange = "CBSE"
		self.last_min = None
		self.symbol = symbol.upper()

	def run(self)-> None:
		self.stream.run()

	def create_target_file_if_not_exists(self, file_path: str)-> None:
		if Path(file_path).is_file() is False:
			with open(file_path, "x") as file:
				file.write(json.dumps([]))

	def write_candle(self, candle: Candle):
		symbol = candle.symbol
		file_path = f"{dir}/../data/{symbol}_bars.json"
		self.create_target_file_if_not_exists(file_path)

		with open(file_path, "r+") as file:
			file_data = json.load(file)
			file_data.append(candle.to_dict())
			file.seek(0)
			json.dump(file_data, file, indent = 4)

	def write_order(self, order: dict):
		file_path = f"{dir}/../data/{self.symbol}_orders.json"
		self.create_target_file_if_not_exists(file_path)

		with open(file_path, "r+") as file:
			file_data = json.load(file)
			file_data.append(order)
			file.seek(0)
			json.dump(file_data, file, indent = 4)

