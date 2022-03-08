from __future__ import annotations
from typing import List, Tuple
import json
from enum import Enum

from src.candle.candle import Candle

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

	def to_dict(self)-> dict:
		return [candle.to_dict() for candle in self.candles]

	def add(self, candle: Candle)-> List[Candle]:
		self.candles.append(candle)
		self.sort_candles()

		return self.candles

	def get_trend(self)-> Trend:
		"""
		Returns the trend as an enum. 

		Possible outputs:

			-Tuple.UP if trend is going up
			
			-Tuple.DOWN if trend is heading down

			-Tuple.NA if trend could not be calculated
		"""
		(lows, highs, _both,) = self.get_trend_reverses()

		if len(highs) < 2 or len(lows) < 2:
			return Trend.NA

		if lows[-1].close > lows[-2].close:
			return Trend.UP
		else:
			return Trend.DOWN

	def get_trend_reverses(self)-> Tuple[List[Candle]]:
		"""
		Returns a tupple containing:

			-The lows reverse candles as a list

			-The highs reverse candles as a list

			-Both highs and lows reverse candles in chronological order as a list
		
		### Example:
		```python
		cc = CandleCollection()
		(lows, highs, both) = cc.get_trend_reverses()
		```
		"""
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
		"""
		Returns boolean: 
		
			-True if the candles in the collection form an up trend

			-False if the candles form a down trend or if the trend cannot be inferred from the current candles
		
		### Example:
		```python
		cc = CandleCollection()
		if cc.is_up_trend():
			pass # do something here
		```
		"""
		return True if self.get_trend() == Trend.UP else False

	def is_down_trend(self)-> bool:
		return True if self.get_trend() == Trend.DOWN else False

	def get_support(self)-> float | None:
		"""
		Returns the support price for the current candles.
		
		Can return None if:

			-There are less than 2 low reverse point candles in the collection
			
			-The last low reverse candle breaks the past support price

		### Example:
		```python
		cc = CandleCollection()
		support = cc.get_support() # 103.55
		```
		"""
		(lows, _highs, _both,) = self.get_trend_reverses()
		if len(lows) < 2:
			return None

		support = lows[-2]
		if lows[-1].close < support.close:
			return None

		return support.close

	def get_resistance(self)-> float | None:
		"""
		Returns the resistance price for the current candles.
		
		Can return None if:

			-There are less than 2 high reverse point candles in the collection
			
			-The last high reverse candle breaks the past resistance price

		### Example:
		```python
		cc = CandleCollection()
		resistance = cc.get_resistance() # 103.55
		```
		"""
		(_lows, highs, _both,) = self.get_trend_reverses()
		if len(highs) < 2:
			return None

		resistance = highs[-2]
		if highs[-1].close > resistance.close:
			return None

		return resistance.close

	def is_impulse(self)-> bool | None:
		if len(self.candles) == 0:
			return None

		(_lows, _highs, both) = self.get_trend_reverses()
		if len(both) == 0:
			last_reverse = self.candles[0]
		else:
			last_reverse = both[-1]

		last_candle = self.candles[-1]

		if last_reverse.timestamp == last_candle.timestamp:
			return False

		if last_reverse.close > last_candle.close:
			return False

		return True


