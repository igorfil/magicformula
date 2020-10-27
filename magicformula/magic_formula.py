from util.stock_filters import *

def calculate_magic_list(stocks: dict, min_roa: float, min_pe: float, max_pe: float, max_cap: int):
    magic_stocks = list(_filter(stocks, min_roa, min_pe, max_pe, max_cap))

    for i, stock in enumerate(sorted(magic_stocks, key=lambda stock: stock["pe"])):
        stock["pe_rank"] = i + 1

    for i, stock in enumerate(sorted(magic_stocks, key=lambda stock: stock["roa"], reverse=True)):
        stock["roa_rank"] = i + 1

    for i, stock in enumerate(sorted(magic_stocks, key=lambda stock: stock["pe_rank"] + stock["roa_rank"])):
        stock["rank"] = i + 1

    return sorted(magic_stocks, key=lambda stock: stock["rank"])

def _filter(stocks: dict, min_roa, min_pe, max_pe, max_market_cap):
    filters=[
        lambda stock: not is_blank(stock.get("name", None)),
        lambda stock: is_allowed_country(stock),
        lambda stock: pe_winthin_range(stock, min_pe, max_pe),
        lambda stock: roa_above_threshold(stock, min_roa),
        lambda stock: market_cap_below_threshold(stock, max_market_cap),
        lambda stock: not has_wrong_type_in_name(stock),
        lambda stock: not wrong_insudtry(stock)
        ]
    return list(filter(lambda x: all([f(x) for f in filters]), stocks.values()))
