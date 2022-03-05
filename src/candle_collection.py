from __future__ import annotations
from typing import List, Tuple
import json
from enum import Enum

from src.candle import Candle

from pprint import pprint


class Trend(Enum):
	UP = "up"
	DOWN = "down"
	NA = "na"


class CandleCollection:
	def __init__(self, candles: List[Candle] = []):
		self.candles = candles
		self.sort_candles()

	def sort_candles(self):
		self.candles = sorted(self.candles, key = lambda d: d.timestamp)

	def load_from_file(self, file: str):
		with open(file, "r") as file:
			data = json.loads(file.read())
			for d in data:
				self.add(Candle.from_dict(d))

	def add(self, candle: Candle)-> List[Candle]:
		self.candles.append(candle)
		self.sort_candles()

		return self.candles

	def get_trend(self)-> Trend:
		(lows, highs, _both,) = self.get_trend_reverses()

		if len(highs) < 2 or len(lows) < 2:
			return Trend.NA

		if lows[-1].close > lows[-2].close:
			return Trend.UP
		else:
			return Trend.DOWN

	def get_trend_reverses(self)-> Tuple[List[Candle]]:
		direction = 0
		prev_candle = self.candles[0]
		highs = []
		lows = []
		reverses = []

		for i, candle in enumerate(self.candles):
			if i == 0:
				continue
			
			current_direction = 0
			if candle.close > prev_candle.close:
				current_direction = 1
			elif candle.close < prev_candle.close:
				current_direction = -1
			else:
				current_direction = 0

			if direction != 0 and direction != current_direction:
				# reverse point found
				if direction > current_direction:
					highs.append(prev_candle)

				if direction < current_direction:
					lows.append(prev_candle)

				reverses.append(prev_candle)

			prev_candle = candle
			direction = current_direction

		return (lows, highs, reverses,)

	def is_up_trend(self)-> bool:
		return True if self.get_trend() == Trend.UP else False

	def is_down_trend(self)-> bool:
		return True if self.get_trend() == Trend.DOWN else False

