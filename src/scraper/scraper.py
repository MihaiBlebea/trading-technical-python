from pprint import pprint

import yfinance as yf
import pandas as pd
from pathlib import Path
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import concurrent.futures

from src.scraper.middleware import cache_in

cur_dir = Path(__file__).parent.resolve()

class Scraper:
	def __init__(self, symbols: list = None):
		self.symbols = symbols if symbols is not None else self.get_symbols()
		self.tickers = yf.Tickers(",".join(self.symbols)).tickers.values()
		
		# self.get_yearly_financials()

	def get_symbols()-> list:
		folder_path = f"{cur_dir}/../../data"
		file_path = f"{folder_path}/symbols.txt"
		if Path(file_path).is_file():
			with open(file_path, "r") as file:
				return [line.rstrip() for line in file]

		table=pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
		symbols =  table[0].to_dict()["Symbol"].values()
		with open(file_path, "w") as file:
			file.write("\n".join(symbols))

		return symbols

	def set_symbols(self, symbols: list)-> None:
		self.symbols = symbols

	@cache_in("quarterly_financials.json")
	def get_ticker_quarterly_financials(self, ticker: yf.Ticker)-> dict:
		symbol = ticker.ticker
		res = {}
		fin = ticker.quarterly_financials.to_dict()
		for key, val in fin.items():
			if isinstance(key, str) is True:
				print(f"Skipping symbol {symbol}...")
				return
			key = key.strftime("%Y-%m-%d")
			res[key] = val

		return res

	@cache_in("info.json")
	def get_ticker_info(self, ticker: yf.Ticker)-> dict:
		return ticker.info

	@cache_in("news.json")
	def get_ticker_news(self, ticker: yf.Ticker)-> dict:
		news = ticker.news
		for n in ticker.news:
			# scrape the article source and fetch image and description
			n = self.scrape_extra_news_data(n)

			n["publishedUTC"] = datetime.fromtimestamp(n["providerPublishTime"]).strftime("%Y-%m-%d")
			n["symbol"] = ticker.ticker.upper()

		return news

	@cache_in("analysis.json")
	def get_ticker_analysis(self, ticker: yf.Ticker)-> dict:
		return ticker.analysis.to_dict()

	@cache_in("quarterly_earnings.json")
	def get_ticker_quarterly_earnings(self, ticker: yf.Ticker)-> dict:
		return ticker.quarterly_earnings.to_dict()

	@cache_in("balance_sheet.json")
	def get_ticker_balance_sheet(self, ticker: yf.Ticker)-> dict:
		symbol = ticker.ticker
		res = {}
		fin = ticker.balance_sheet.to_dict()
		for key, val in fin.items():
			if isinstance(key, str) is True:
				print(f"Skipping symbol {symbol}...")
				return
			key = key.strftime("%Y-%m-%d")
			res[key] = val

		return res

	def __scrape_single(self, ticker: yf.Ticker, index: int = None)-> None:
		if index is not None:
			print(f"{index}/{len(self.tickers)} Fetching data for {ticker.ticker}")
		self.get_ticker_quarterly_financials(ticker)
		self.get_ticker_info(ticker)
		self.get_ticker_news(ticker)
		self.get_ticker_analysis(ticker)
		self.get_ticker_quarterly_earnings(ticker)
		self.get_ticker_balance_sheet(ticker)

	def scrape_data(self)-> None:
		count = 1
		for ticker in self.tickers:
			self.__scrape_single(ticker, count)
			count += 1

		return None

	def scrape_data_concurrent(self)-> None:
		count = 1
		with concurrent.futures.ThreadPoolExecutor() as tpe:
			for ticker in self.tickers:
				tpe.submit(self.__scrape_single, ticker, count)
				count += 1

	def scrape_extra_news_data(self, news: dict)-> dict:
		response = requests.get(news["link"])
		soup = BeautifulSoup(response.text, features="lxml")

		metas = soup.find_all("meta")

		images = [ meta.attrs["content"] for meta in metas if "property" in meta.attrs and meta.attrs["property"] == "og:image" ]
		news["feature_image"] = images[0] if len(images) > 0 else "https://www.altfi.com/images/companies/yahoo-finance.png"

		return news

if __name__ == "__main__":
	start_time = datetime.now()
	# s = Scraper()
	s = Scraper(["AAPL"])
	s.scrape_data_concurrent()

	print(datetime.now() - start_time)