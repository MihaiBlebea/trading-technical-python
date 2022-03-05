from pprint import pprint

from src.stream_base import BaseStreamer
from src.candle import Candle

class Streamer(BaseStreamer):
	def __init__(self, symbol: str):
		super().__init__(symbol)

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
		self.write_data(candle)


if __name__ == "__main__":
	s = Streamer("BTCUSD")
	s.run()
