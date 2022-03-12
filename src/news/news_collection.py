from __future__ import annotations
from typing import List
import json
from pathlib import Path

from src.news.news import News


class NewsCollection:

	def __init__(self, news: List[News] = []):
		self.news = news

	def load_from_file(self, file_path: str)-> List[News]:
		with open(file_path, "r") as file:
			data = json.loads(file.read())
			self.news = [News.from_dict(d) for d in data]

		return self.news

	def load_from_folder(self, folder_path: str)-> List[News]:
		news = []
		for path in Path(folder_path).iterdir():
			try:
				if path.is_dir():
					news += (self.load_from_file(f"{path}/news.json"))
			except:
				print(f"Could not load from {path}")

		self.news = news

		return self.news

	def to_dict(self)-> List[dict]:
		return [n.to_dict() for n in self.news]

	def get_today(self)-> List[News]:
		news = [ n for n in self.news if n.is_today() ]
		return sorted(news, key = lambda d: d.publish_timestamp)

	def get_symbol(self, symbol: str)-> List[News]:
		news = [ n for n in self.news if n.is_symbol(symbol) ]
		return sorted(news, key = lambda d: d.publish_timestamp)

if __name__ == "__main__":
	from pprint import pprint
	nc = NewsCollection()
	nc.load_from_folder("./data")
	pprint(nc.get_today())


