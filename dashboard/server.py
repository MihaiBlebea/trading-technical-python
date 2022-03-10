from flask import (
	Flask, 
	jsonify, 
	request, 
	redirect, 
	abort, 
	send_from_directory, 
	render_template
)
from pathlib import Path

from src.config import get_key
from src.scraper.scraper import Scraper
from src.candle.candle_collection import CandleCollection
from src.news.news_collection import NewsCollection
from src.client import Client


cur_dir = Path(__file__).parent.resolve()

app = Flask(__name__, static_url_path="/static")

@app.before_request
def before_request_func():
	pass
	# This runs before each request. Do validation here

@app.route("/home/<symbol>")
def index(symbol):
	symbol = symbol.upper()
	news_file_path = f"{cur_dir}/../data/{symbol}/news.json"
	if Path(news_file_path).is_file() == False:
		scraper = Scraper([symbol])
		scraper.scrape_data()

	news_collection = NewsCollection()
	news_collection.load_from_file(news_file_path)

	return render_template("index.html", data={
		"symbol": symbol.upper(),
		"news": news_collection.to_dict()
	})

@app.route("/order", methods=["GET", "POST"])
def get_order_form():
	if request.method == "GET":
		return render_template("order_form.html")
	else:
		symbol = request.form["symbol"].upper()
		quantity = int(request.form["quantity"])
		buy_price = float(request.form["buy_price"])
		stop_loss = float(request.form["stop_loss"])
		take_profit = float(request.form["take_profit"])

		client = Client()
		client.place_bracket_order(
			symbol,
			quantity,
			buy_price,
			take_profit,
			stop_loss
		)

		return redirect("/home/aapl")

@app.route("/js/<path:path>")
def send_js(path):
    return send_from_directory("./static/js", path)

@app.route("/api/candles/<symbol>", methods=["GET"])
def get_candles(symbol):
	symbol = symbol.upper()
	cc = CandleCollection()
	cc.load_from_file(f"{cur_dir}/../data/{symbol}_bars.json")
	return jsonify(cc.to_dict())

@app.route("/api/news/<symbol>", methods=["GET"])
def get_news(symbol):
	symbol = symbol.upper()
	news_collection = NewsCollection()
	news_collection.load_from_file(f"{cur_dir}/../data/{symbol}/news.json")
	return jsonify(news_collection.to_dict())


if __name__ == "__main__":
	app.run(host="0.0.0.0", port=int(get_key("HTTP_PORT")), debug=True)