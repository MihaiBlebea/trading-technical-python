import yfinance as yf
from pathlib import Path
from datetime import datetime
import simplejson as json

def cache_in(file_name: str):
	def outer(cb):
		def inner(self, ticker: yf.Ticker):
			name = file_name.split('.')[0].replace("_", " ")
			
			# check if cache exists and return if found
			symbol = ticker.ticker
			cur_dir = Path(__file__).parent.resolve()
			folder_path = f"{cur_dir}/../../data/" + symbol
			file_path = f"{folder_path}/{file_name}"
			if Path(file_path).is_file():
				with open(file_path, "r") as file:
					print(f"\t- Fetching cached {name} data for {symbol} ✅")
					return json.loads(file.read())
			# check if cache exists and return if found
			
			try:
				res = cb(self, ticker)
				
				print(f"\t- Scraped {name} data for {symbol} ✅")
			except:
				print(f"\t- Failed to scrape {name} data for {symbol} ❌")

			# cache the response
			Path(folder_path).mkdir(parents=True, exist_ok=True)
			with open(file_path, "w") as file:
				file.write(json.dumps(res, ignore_nan=True, indent=4, default=convertor))
			# cache the response

			return res
		return inner
	return outer

def convertor(o):
    if isinstance(o, datetime):
        return o.__str__()