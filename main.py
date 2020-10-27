import argparse
from datetime import datetime
import os

from data_source.finnhub import Finnhub
from data_source.finnhub_data_adapter import map_stock_data, map_stock_price, map_financial_data
from registry.stocks_registry import StocksRegistry
from magicformula.magic_formula import calculate_magic_list
from reporter.html_reporter import create_report

def parse_args():
    defaults = {
        "force_update": False,
        "min_roa": 20.0,
        "min_pe": 4.0,
        "max_pe": 40.0,
        "max_cap": 1000
    }

    parser = argparse.ArgumentParser(description='Magic Formula calculator')
    parser.add_argument('--api-key', dest='api_key', help='Finnhub API key')

    parser.add_argument('--force-update', dest='force_update', action='store_true', help="Force update of stock data")
    parser.add_argument('--min-roa', dest='min_roa', help="Min ROA for magic formula calculation")
    parser.add_argument('--min-pe', dest='min_pe', help="Min P/E for magic formula calculation")
    parser.add_argument('--max-pe', dest='max_pe', help="Max P/E for magic formula calculation")
    parser.add_argument('--max-cap', dest='max_cap', help="Max market cap for magic formula calculation")

    parser.set_defaults(**defaults)

    return vars(parser.parse_args())

def generate_report_filename():
    REPORTS_FOLDER = "./reports"
    today = datetime.today().strftime('%Y-%m-%d')

    return os.path.join(REPORTS_FOLDER, today + ".html")

def show_report(report):
    os.system("open " + report)

def main():
    config = parse_args()

    f = Finnhub(config["api_key"], map_stock_data, map_stock_price, map_financial_data)
    r = StocksRegistry(f, os.path.abspath("data/stocks.json"))

    r.load_stocks(["US"])
    r.enrich_stock_data(force_update=config["force_update"])

    magic_list = calculate_magic_list(r.stocks, float(config["min_roa"]), float(config["min_pe"]), float(config["max_pe"]), int(config["max_cap"]))

    report_file = generate_report_filename()
    create_report(magic_list, report_file)
    show_report(report_file)

if __name__ == "__main__":
    main()