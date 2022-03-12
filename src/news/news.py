from __future__ import annotations
from datetime import datetime


class News:

	def __init__(self):
		self.link = None
		self.symbol = None
		self.publish_timestamp = None
		self.published_utc = None
		self.publisher = None
		self.title = None
		self.type = None
		self.uuid = None
		self.feature_image = None

	def from_dict(data: dict)-> News:
		n = News()
		n.link = data["link"]
		n.symbol = data["symbol"]
		n.publish_timestamp = data["providerPublishTime"]
		n.published_utc = data["publishedUTC"]
		n.publisher = data["publisher"]
		n.title = data["title"]
		n.type = data["type"]
		n.uuid = data["uuid"]
		n.feature_image = data["feature_image"]

		return n

	def to_dict(self)-> dict:
		return self.__dict__

	def is_today(self)-> bool:
		return self.published_utc == datetime.now().strftime("%Y-%m-%d")

	def is_symbol(self, symbol: str)-> bool:
		return self.symbol.upper() == symbol.upper()