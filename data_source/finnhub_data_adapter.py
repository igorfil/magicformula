from functools import partial
from data_source.data_adapter import pick_keys

stock_data_keys = {
    "country": "country",
    "finnhubIndustry": "industry",
    "logo": "logo",
    "name": "name",
    "ticker": "ticker",
    "weburl": "url",
    "marketCapitalization": "market_cap"
}

stock_price_keys = {
    "c": "price"
}

financial_data_keys = {
    "52WeekHigh": "price_high",
    "52WeekLow": "price_low",
    "peNormalizedAnnual": "pe",
    "priceRelativeToS&P50052Week": "vs_snp500",
    "roaRfy": "roa",
    "marketCapitalization": "market_cap"
}

map_stock_data = partial(pick_keys, key_mapping=stock_data_keys)
map_stock_price = partial(pick_keys, key_mapping=stock_price_keys)
map_financial_data = partial(pick_keys, key_mapping=financial_data_keys)
