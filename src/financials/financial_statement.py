from __future__ import annotations
from pathlib import Path
import json


class FinancialStatement:

	def from_dict(data: dict)-> FinancialStatement:
		fs = FinancialStatement()
		for key, val in data.items():
			key = key.lower().replace(" ", "_")
			setattr(fs, key, val)

		return fs
	
	def to_dict(self)-> dict:
		return self.__dict__


