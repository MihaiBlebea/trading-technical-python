import unittest
from typing import List

from src.candle_collection import CandleCollection, Trend
from src.candle import Candle


class TestCandleCollection(unittest.TestCase):

	def test_load_from_file(self):
		cc = CandleCollection()
		cc.load_from_file("./data/BTCUSD_bars.json")

		self.assertEqual(len(cc.candles), 10)

	def test_up_trend(self):
		cc = CandleCollection(self.gen_candles_from_seq(
			[1, 2, 3, 4, 2, 1, 3, 5, 4, 3, 6]
		))
		self.assertEqual(cc.get_trend(), Trend.UP)
	
	def test_down_trend(self):
		cc = CandleCollection(self.gen_candles_from_seq(
			[1, 2, 1, 3, 5, -1, 0, 1]
		))
		self.assertEqual(cc.get_trend(), Trend.DOWN)

	def test_trend_insufficient_reverses(self):
		cc = CandleCollection(self.gen_candles_from_seq(
			[1, 2, 3, 4, 5, 4, 2, 1, -1, 4, 4]
		))
		self.assertEqual(cc.get_trend(), Trend.NA)

	def test_support_price_can_be_found(self):
		cc = CandleCollection(self.gen_candles_from_seq(
			[4, 2, 4, 3, 5, 10]
		))
		support = cc.get_support()
		self.assertEqual(support, 102)

	def test_support_price_cannot_be_found(self):
		cc = CandleCollection(self.gen_candles_from_seq(
			[4, 2, 4, 5, 10]
		))
		support = cc.get_support()
		self.assertIsNone(support)

	def test_support_price_is_broken_by_candle(self):
		cc = CandleCollection(self.gen_candles_from_seq(
			[4, 2, 4, -1, 5, 10]
		))
		support = cc.get_support()
		self.assertIsNone(support)

	def test_resistance_price_can_be_found(self):
		cc = CandleCollection(self.gen_candles_from_seq(
			[1, 2, 3, 4, 2, 4, -1]
		))
		resistance = cc.get_resistance()
		self.assertEqual(resistance, 104)

	def test_resistance_price_cannot_be_found(self):
		cc = CandleCollection(self.gen_candles_from_seq(
			[1, 2, 3, 4, 2, -1]
		))
		resistance = cc.get_resistance()
		self.assertIsNone(resistance)

	def test_resistance_price_is_broken_by_candle(self):
		cc = CandleCollection(self.gen_candles_from_seq(
			[1, 2, 3, 4, 2, 6, -1]
		))
		resistance = cc.get_resistance()
		self.assertIsNone(resistance)

	def gen_candles_from_seq(self, seq: List[int])-> List[Candle]:
		return [
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


if __name__ == "__main__":
    unittest.main()