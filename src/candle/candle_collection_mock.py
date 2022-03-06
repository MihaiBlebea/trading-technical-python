from src.candle.candle_collection import CandleCollection
from src.candle.candle import Candle

import random


class CandleCollectionMock(CandleCollection):
	def __init__(self):
		super().__init__()

	def load_random_candles(self)-> None:
		seq = [random.randrange(1, 50, 1) for i in range(7)]
		candles = [
			Candle.from_dict({
				"symbol": "BTCUSD",
				"open": 0,
				"close": 100 + v,
				"high": 0,
				"low": 0,
				"volume": 1,
				"timestamp": 1646489385000 + i,
				"trade_count": 2,
			}) for i, v in enumerate(seq) if v > -100
		]

		for candle in candles:
			self.add(candle)

	def print(self)-> None:
		(_, _ , reverses,) = self.get_trend_reverses()
		
		fmt = ""
		prev_reverse = reverses[0]
		for i, r in enumerate(reverses):
			if i == 0:
				fmt += str(r.close)

			if prev_reverse.close > r.close:
				fmt += f" \\ {r.close}"
			elif prev_reverse.close < r.close:
				fmt += f" / {r.close}"
			else:
				fmt += f" - {r.close}"

			prev_reverse = r

		print(fmt)

if __name__ == "__main__":
	ccm = CandleCollectionMock()
	ccm.load_random_candles()
	ccm.print()
