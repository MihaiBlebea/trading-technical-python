from __future__ import annotations

from pprint import pprint
from datetime import datetime, timedelta

import alpaca_trade_api as trade_api
from src.config import get_key


class Client():

	def __init__(self):
		self.api_client = trade_api.REST(
			key_id=get_key("ALPACA_KEY_ID"),
			secret_key=get_key("ALPACA_SECRET_KEY"),
			base_url=get_key("ALPACA_BASE_URL"),
		)

	def get_amount_to_invest(self)-> float | None:
		account = self.api_client.get_account()
		cash = float(account.cash)
		if cash < 1:
			print(f"Insufficient cash balance ${cash}")
			return None

		invest_cash = round(cash / 2, 2)
		print(f"Cash available to invest ${invest_cash}")

		return invest_cash

	def place_bracket_order(self, symbol: str, buy_price: float)-> None | trade_api.rest.Order:
		invest_cash = self.get_amount_to_invest()
		if invest_cash is None:
			return None

		take_profit = buy_price + buy_price * 0.01
		stop_price = buy_price - buy_price * 0.01
		print(f"Take profit ${take_profit}")
		print(f"Stop price ${stop_price}")

		order = self.api_client.submit_order(
			side="buy",
			symbol=symbol,
			type="market",
			qty=1,
			time_in_force="gtc",
			order_class="bracket",
			take_profit={"limit_price": take_profit},
			stop_loss={
				"stop_price": stop_price,
				# "limit_price": 298.5
			}
		)

		return order

	def place_buy_order(self, symbol: str, buy_price: float)-> None | trade_api.rest.Order:
		invest_cash = self.get_amount_to_invest()
		if invest_cash is None:
			return None

		order = self.api_client.submit_order(
			client_order_id="1",
			side="buy",
			symbol=symbol,
			type="market",
			qty=1,
			time_in_force="day",
		)

		return order

	def place_sell_order(self, symbol: str, limit_price: float = None)-> None | trade_api.rest.Order:
		order = self.api_client.submit_order(
			client_order_id="1",
			side="sell",
			symbol=symbol,
			limit_price=limit_price,
			type="market" if limit_price is None else "limit",
			qty=1,
			time_in_force="day",
		)

		return order


if __name__ == "__main__":
	c = Client()
	pprint(c)
	order = c.place_buy_order("BTCUSD", 38363.80)
	print(order)