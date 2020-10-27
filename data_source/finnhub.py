import json
import requests
import time

class Finnhub:
    def __init__(self, api_key, stock_data_adapter, stock_price_adapter, financial_data_adapter):
        self.api_key = api_key
        self.stock_data_adapter = stock_data_adapter
        self.stock_price_adapter = stock_price_adapter
        self.financial_data_adapter = financial_data_adapter

        self.tokens_left = 60
        self.next_tokens_reset = int(time.time())

        self.verify()

    def verify(self):
        url = "https://finnhub.io/api/v1/quote?symbol=AAPL&token={api_key}"
        result = requests.get(url.format(api_key=self.api_key))
        result.raise_for_status()
        self.tokens_left = int(result.headers["X-Ratelimit-Remaining"])
        self.next_tokens_reset = int(result.headers["X-Ratelimit-Reset"])

    def get_stocks(self, exchange):
        url = "https://finnhub.io/api/v1/stock/symbol?exchange={exchange}&token={api_key}"
        return self._fetch_url(url.format(exchange=exchange, api_key=self.api_key))

    def get_company_profile(self, symbol):
        url = "https://finnhub.io/api/v1/stock/profile2?symbol={symbol}&token={api_key}"
        raw_data = self._fetch_url(url.format(symbol=symbol, api_key=self.api_key))

        return self.stock_data_adapter(raw_data)

    def get_stock_financial_data(self, symbol):
        url = "https://finnhub.io/api/v1/stock/metric?metric=all&symbol={symbol}&token={api_key}"
        raw_data = self._fetch_url(url.format(symbol=symbol, api_key=self.api_key))
        return self.financial_data_adapter(raw_data["metric"])

    def get_stock_price(self, symbol):
        url = "https://finnhub.io/api/v1/quote?symbol={symbol}&token={api_key}"
        raw_data = self._fetch_url(url.format(symbol=symbol, api_key=self.api_key))
        return self.stock_price_adapter(raw_data)

    def _wait_time(self):
        return (self.next_tokens_reset + 40 - int(time.time()) ) / max(self.tokens_left, 1)

    def _fetch_url(self, url):
        retries_left = 5

        while retries_left > 0:
            time.sleep(self._wait_time())

            result = requests.get(url)

            self.tokens_left = int(result.headers.get("X-Ratelimit-Remaining", self.tokens_left))
            self.next_tokens_reset = int(result.headers.get("X-Ratelimit-Reset", self.next_tokens_reset))

            if result.status_code == 200:
                try:
                    return json.loads(result.text)
                except:
                    return {}
            else:
                print("Error getting data from {url}".format(url=url))
                print(result.reason)
                retries_left -= 1
                time.sleep(5)

        raise(Exception("Cannot load data from Finnhub"))

