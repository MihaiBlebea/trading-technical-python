from __future__ import annotations
from typing import List
import json

from src.ledger.order import Order


class Ledger:

	def __init__(self, orders: List[Order] = []) -> None:
		self.orders = orders

	def load_from_file(self, file: str)-> List[Order]:
		with open(file, "r") as file:
			data = json.loads(file.read())
			self.orders = [Order.from_dict(d) for d in data]

	def add(self, order: Order)-> List[Order]:
		self.orders.append(order)

		return self.orders