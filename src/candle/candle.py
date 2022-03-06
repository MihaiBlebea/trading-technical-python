from __future__ import annotations
from datetime import datetime, timezone


class Candle:
	def __init__(self):
		self.symbol = None
		self.open = None
		self.close = None
		self.high = None
		self.low = None
		self.volume = None
		self.trade_count = None
		self.timestamp = None
		self.datetime = None

	def from_dict(data: dict)-> Candle:
		c = Candle()
		c.symbol = str(data["symbol"])
		c.open = float(data["open"])
		c.close = float(data["close"])
		c.high = float(data["high"])
		c.low = float(data["low"])
		c.volume = float(data["volume"])
		c.trade_count = int(data["trade_count"])
		c.timestamp = int(data["timestamp"])

		ts_in_seconds = data["timestamp"] // 1000000000
		dt = datetime.fromtimestamp(ts_in_seconds, tz=timezone.utc)
		c.datetime = dt.strftime("%Y-%m-%d %H:%M:%S")

		return c

	def to_dict(self)-> dict:
		return {
			"symbol": self.symbol,
			"open": self.open,
			"close": self.close,
			"high": self.high,
			"low": self.low,
			"volume": self.volume,
			"timestamp": self.timestamp,
			"trade_count": self.trade_count,
			"datetime": self.datetime
		}

