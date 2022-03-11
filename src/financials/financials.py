from __future__ import annotations
from typing import List
from pathlib import Path
import json

from src.financials.financial_statement import FinancialStatement


class Financials:

	def __init__(self):
		self.financial_statements = []

	def load_from_file(self, file_path: str)-> List[FinancialStatement] | None:
		if Path(file_path).is_file() == False:
			return None

		with open(file_path, "r") as file:
			data = json.loads(file.read())
			if data is None:
				print(f"Skip symbol {file_path}")
				return None

			for key, val in data.items():
				val["date"] = key

				financial = FinancialStatement.from_dict(val)
				if financial is None:
					continue

				self.add_financial_statement(financial)

	def add_financial_statement(self, financial_statement: FinancialStatement)-> List[FinancialStatement]:
		self.financial_statements.append(financial_statement)
		self.financial_statements = sorted(self.financial_statements, key = lambda d: d.date)

		return self.financial_statements

	def is_net_profitable(self)-> bool:
		return self.financial_statements[-1].net_income > 0

if __name__ == "__main__":
	from pprint import pprint
	from src.scraper.scraper import Scraper
	symbols = Scraper.get_symbols()

	results = []
	for symbol in symbols:
		fs = Financials()
		res = fs.load_from_file(f"./data/{symbol}/quarterly_financials.json")
		if res is None:
			continue

		if fs.is_net_profitable() == False:
			results.append(fs)

	pprint(results)