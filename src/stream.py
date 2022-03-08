from pprint import pprint

from src.stream_base import BaseStreamer
from src.candle.candle import Candle
from src.candle.candle_collection import CandleCollection
from src.client import Client


class Streamer(BaseStreamer):

	def __init__(self, client: Client, symbol: str):
		super().__init__(symbol)

		self.client = client
		self.cc = CandleCollection()

		self.stream.subscribe_trade_updates(self.crypto_trade_handler)
		self.stream.subscribe_crypto_bars(self.crypto_bars_handler, self.symbol)

	def run(self)-> None:
		self.stream.run()

	async def crypto_trade_handler(self, data):
		event_type = data.event

		message = None
		if event_type == "fill" or event_type == "partial_fill":
			print(data.order)
		elif event_type == "rejected" or event_type == "canceled":
			symbol = data.order["symbol"]
			message = f"Order {symbol} has been rejected"
		elif event_type != "new":
			message = f"Unexpected order event type {event_type} received"

		if message is None:
			return
			
	async def crypto_bars_handler(self, data):
		if data.exchange != self.exchange:
			return
		candle = Candle.from_dict(data.__dict__["_raw"])
		self.cc.add(candle)
		# pprint(self.cc.candles)
		# print(f"Resistance {self.cc.get_resistance()}")
		# print(f"Support {self.cc.get_support()}")
		self.write_candle(candle)

		# order = self.client.place_buy_order(self.symbol, candle.close)
		# self.write_order(order.__dict__["_raw"])


if __name__ == "__main__":
	s = Streamer(Client(), "BTCUSD")
	s.run()
