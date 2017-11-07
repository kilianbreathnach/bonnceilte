import json
import requests
import multiprocessing
from scrape_bot import ScraperBot


# first let's find all the markets we can pull from
r = requests.get("https://bittrex.com/api/v1.1/public/getmarkets")

markets = json.loads(r.content.decode("UTF-8"))["result"]

market_dir = "../bittrex/markets"

for market in markets:

    if market["IsActive"]:
        market_str = market["BaseCurrency"] + "-" + market["MarketCurrency"]
        dir_str = market["BaseCurrency"] + "_" + market["MarketCurrency"]

        if not os.path.exists(market_dir + dir_str):
            os.makedirs(market_dir + dir_str)

