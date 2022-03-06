from __future__ import annotations

class Order:

	def __init__(self) -> None:
		self.id = None
		self.symbol = None
		self.qty = None
		self.order_type = None
		self.side = None
		self.time_in_force = None
		self.status = None
		self.filled_avg_price = None
		self.created_at = None
		self.filled_at = None

	def from_dict(data: dict)-> Order:
		o = Order()
		o.id = data["id"]
		o.symbol = data["symbol"]
		o.qty = data["qty"]
		o.order_type = data["order_type"]
		o.side = data["side"]
		o.time_in_force = data["time_in_force"]
		o.status = data["status"]
		o.filled_avg_price = data["filled_avg_price"]
		o.created_at = data["created_at"]
		o.filled_at = data["filled_at"]

		return o