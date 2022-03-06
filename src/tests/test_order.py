import unittest
from typing import List
import json

from src.ledger.order import Order


class TestOrder(unittest.TestCase):

	def test_create_order_from_dict(self):
		data = {
			"id": "61e69015-8549-4bfd-b9c3-01e75843f47d",
			"client_order_id": "eb9e2aaa-f71a-4f51-b5b4-52a6c565dad4",
			"created_at": "2021-03-16T18:38:01.942282Z",
			"updated_at": "2021-03-16T18:38:01.942282Z",
			"submitted_at": "2021-03-16T18:38:01.937734Z",
			"filled_at": None,
			"expired_at": None,
			"canceled_at": None,
			"failed_at": None,
			"replaced_at": None,
			"replaced_by": None,
			"replaces": None,
			"asset_id": "b0b6dd9d-8b9b-48a9-ba46-b9d54906e415",
			"symbol": "AAPL",
			"asset_class": "us_equity",
			"notional": "500",
			"qty": 2,
			"filled_qty": "0",
			"filled_avg_price": None,
			"order_class": "",
			"order_type": "market",
			"type": "market",
			"side": "buy",
			"time_in_force": "day",
			"limit_price": None,
			"stop_price": None,
			"status": "accepted"
		}
		order = Order.from_dict(data)

		self.assertEqual(data["id"], order.id)
		self.assertEqual(data["qty"], order.qty)