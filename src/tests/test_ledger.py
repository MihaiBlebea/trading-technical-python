import unittest
from typing import List
import json

from src.ledger.order import Order
from src.ledger.ledger import Ledger


class TestLedger(unittest.TestCase):

	def test_add_order_to_ledger(self):
		ledger = Ledger()

		for _i in range(20):
			ledger.add(self.gen_order())

		self.assertEqual(len(ledger.orders), 20)

	def gen_order(self)-> Order:
		return Order.from_dict({
			"id": "61e69015-8549-4bfd-b9c3-01e75843f47d",
			"created_at": "2021-03-16T18:38:01.942282Z",
			"submitted_at": "2021-03-16T18:38:01.937734Z",
			"filled_at": None,
			"symbol": "AAPL",
			"qty": 2,
			"filled_avg_price": None,
			"order_type": "market",
			"side": "buy",
			"time_in_force": "day",
			"limit_price": None,
			"status": "accepted"
		})