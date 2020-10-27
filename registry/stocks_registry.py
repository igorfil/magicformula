import json
import time

from util.stock_filters import *

blacklist=["FTV#", "VNT#"]

class StocksRegistry:
    def __init__(self, data_source, data_file):
        self.data_source = data_source
        self.data_file = data_file
        self.stocks = {}
        self._load()

    def load_stocks(self, exchanges):
        new_stocks = {}

        for exchange in exchanges:
            exchange_stocks = self.data_source.get_stocks(exchange)
            for stock in exchange_stocks:
                ticker = stock["symbol"]
                if ticker not in self.stocks.keys() and \
                    stock["type"] != "ETF":
                    new_stocks[ticker] = {}

        self.stocks = {**self.stocks, **new_stocks}
        self._save()

    def _now(self) -> int:
        return int(time.time())

    def enrich_stock_data(self, force_update=False):
        enriched = 0
        for symbol, company_data in self.stocks.items():
            if symbol not in blacklist and (force_update or self._need_to_enrich(company_data)):
                print("Enriching " + symbol)

                info = self.data_source.get_company_profile(symbol)
                financial_data = self.data_source.get_stock_financial_data(symbol)
                price = self.data_source.get_stock_price(symbol)

                last_update = {"last_update": self._now()}

                new_record = {**company_data, **info, **financial_data, **price, **last_update}
                self.stocks[symbol] = new_record

                enriched += 1
                if enriched % 10 == 0:
                    self._save()

        self._save()

    def _need_to_enrich(self, company_data):
        no_data = self._has_no_data(company_data)
        wrong_stock = self._never_update(company_data)
        time_to_update = self._time_to_update(company_data)
        in_blacklist = self._in_blacklist(company_data)

        result = no_data or (not wrong_stock and time_to_update and not in_blacklist)

        return result

    def _in_blacklist(self, company_data):
        return company_data.get("ticker", None) in blacklist

    def _has_no_data(self, company_data):
        return company_data.get("last_update", None) is None

    def _never_update(self, company_data):
        return (not is_allowed_country(company_data)) or has_wrong_type_in_name(company_data)

    def _time_to_update(self, company_data):
        day = 60 * 60 * 24

        return (market_cap_below_threshold(company_data, 1000) and int(company_data.get("last_update", 0)) + 15 * day < self._now()) \
            or ((not market_cap_below_threshold(company_data, 1000)) and int(company_data.get("last_update", 0)) + 90 * day < self._now())

    def _save(self):
        print("Saving data")

        with open(self.data_file, 'w') as fp:
            json.dump(self.stocks, fp, indent=4)

    def _load(self):
        print("Loading data")
        with open(self.data_file, 'r') as fp:
            self.stocks = json.load(fp)