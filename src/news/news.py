from __future__ import annotations


class News:
	def from_dict(data: dict)-> News:
		n = News()
		n.link = data["link"]
		n.publish_timestamp = data["providerPublishTime"]
		n.published_utc = data["publishedUTC"]
		n.publisher = data["publisher"]
		n.title = data["title"]
		n.type = data["type"]
		n.uuid = data["uuid"]

		return n

	def to_dict(self)-> dict:
		return self.__dict__