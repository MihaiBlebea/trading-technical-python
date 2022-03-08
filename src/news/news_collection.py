from __future__ import annotations
from typing import List
import json

from src.news.news import News

class NewsCollection:

	def __init__(self, news: List[News] = []):
		self.news = news

	def load_from_file(self, file_path: str)-> List[News]:
		with open(file_path, "r") as file:
			data = json.loads(file.read())
			self.news = [News.from_dict(d) for d in data]

		return self.news

	def to_dict(self)-> List[dict]:
		return [n.to_dict() for n in self.news]


