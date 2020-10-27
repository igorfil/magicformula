import plotly.express as px
from plotly.io import to_html
import numpy as np
import pandas as pd

def create_chart(stocks):
    df = pd.DataFrame.from_dict(stocks_for_chart(stocks))

    plot = px.scatter(df, x="roa", y="pe", color="name", size='market_cap', hover_data=['name'])
    plot.update_xaxes(autorange="reversed")
    return to_html(plot, full_html=False)

def stocks_for_chart(stocks):
    fields = ["name", "market_cap", "pe", "roa"]

    return [{ key: stock.get(key, "") for key in fields} for stock in stocks ]