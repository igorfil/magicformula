from jinja2 import Template
from reporter.charts import create_chart


def create_report(stocks: list, report_file: str):
    template = Template(open('reporter/template.html').read())

    chart = create_chart(stocks)

    for s in stocks:
        s["market_cap"] = str(int(s["market_cap"])) + "M"

    rendered = template.render(stocks = stocks, chart=chart)

    _save_report(rendered, report_file)

def _save_report(report, file) -> str:
    with open(file, 'w') as f:
        f.write(report)