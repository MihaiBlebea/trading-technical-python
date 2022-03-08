from flask import Flask, jsonify, abort, send_from_directory, render_template
from pathlib import Path

from src.config import get_key
from src.candle.candle_collection import CandleCollection
from src.news.news_collection import NewsCollection

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
		return abort(404)

	news_collection = NewsCollection()
	news_collection.load_from_file(news_file_path)

	return render_template("index.html", data={
		"symbol": symbol.upper(),
		"news": news_collection.to_dict()
	})

@app.route("/js/<path:path>")
def send_js(path):
    return send_from_directory("./static/js", path)

@app.route("/api/candles/<symbol>", methods=["GET"])
def get_candles(symbol):
	symbol = symbol.upper()
	cc = CandleCollection()
	cc.load_from_file(f"{cur_dir}/../data/BTCUSD_bars.json")
	return jsonify(cc.to_dict())

@app.route("/api/news/<symbol>", methods=["GET"])
def get_news(symbol):
	symbol = symbol.upper()
	news_collection = NewsCollection()
	news_collection.load_from_file(f"{cur_dir}/../data/{symbol}/news.json")
	return jsonify(news_collection.to_dict())


if __name__ == "__main__":
	app.run(host="0.0.0.0", port=int(get_key("HTTP_PORT")), debug=True)