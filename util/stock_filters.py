import re

def pe_winthin_range(stock, min_pe, max_pe):
    pe = stock.get("pe", None)
    return pe is not None and pe != "" and float(pe) <= max_pe and float(pe) >= min_pe

def roa_above_threshold(stock, threshold):
    roa = stock.get("roa", None)
    return roa is not None and roa != "" and float(roa) >= threshold

def market_cap_below_threshold(stock, threshold):
    market_cap = stock.get("market_cap", None)
    return market_cap is not None and market_cap != "" and float(market_cap) <= threshold

def is_allowed_country(stock):
    allowed_countries=["CA", "US"]
    return stock.get("country", "") in allowed_countries

def has_wrong_type_in_name(stock):
    name = stock.get("name", "")
    regex = r"^.*( Fund| Trust| ETF| crypto| bitcoin| REIT).*$"
    matches = re.search(regex, name, re.IGNORECASE)

    if matches or '#' in name:
        return True
    return False

def wrong_insudtry(stock):
    name = stock.get("industry", "")
    regex = r"^.*(Financial Services).*$"
    matches = re.search(regex, name, re.IGNORECASE)

    if matches:
        return True
    return False

def is_blank (value):
    if value and value.strip():
        return False
    return True

