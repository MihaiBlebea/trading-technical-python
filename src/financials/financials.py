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
			for key, val in data.items():
				val["date"] = key

				financial = FinancialStatement.from_dict(val)
				if financial is None:
					continue

				self.add_financial_statement(financial)

	def add_financial_statement(
		self, financial_statement: FinancialStatement)-> List[FinancialStatement]:

		self.financial_statements.append(financial_statement)
		self.financial_statements = sorted(self.financial_statements, key = lambda d: d.date)

		return self.financial_statements

	def is_profitable(self)-> bool:
		print(self.financial_statements[-1].to_dict())
		return self.financial_statements[-1].net_income > 0

if __name__ == "__main__":
	from pprint import pprint
	fs = Financials()
	fs.load_from_file("./data/DDOG/quarterly_financials.json")
	pprint(fs.is_profitable())