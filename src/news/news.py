from __future__ import annotations


class News:

	def __init__(self):
		self.link = None
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