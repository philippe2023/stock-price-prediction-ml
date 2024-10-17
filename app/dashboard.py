import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import date


st.title("My Dashboard")

stocks = (
    'AAPL', 'MSFT', 'AMZN', 'GOOGL', 'GOOG', 'FB', 'BRK.B', 'JNJ', 'NVDA', 'JPM', 'UNH', 'V', 'PG', 'HD',
    'MA', 'PFE', 'BAC', 'DIS', 'VZ', 'KO', 'NFLX', 'INTC', 'MRK', 'CSCO', 'T', 'CMCSA', 'CVX', 'XOM', 'PEP', 'ABT',
    'ADBE', 'WMT', 'NKE', 'PYPL', 'TMO', 'CRM', 'ORCL', 'MCD', 'MDT', 'COST', 'AXP', 'LLY', 'BMY', 'QCOM',
    'DHR', 'TXN', 'UNP', 'UPS', 'LIN', 'SBUX', 'HON', 'AVGO', 'AMGN', 'CAT', 'AMT', 'GILD', 'GS', 'SCHW',
    'BKNG', 'MS', 'ISRG', 'SPGI', 'ZTS', 'INTU', 'FIS', 'USB', 'RTX', 'DE', 'C', 'BLK', 'PLD', 'MMM', 'IBM', 'NOW',
    'SYK', 'CB', 'MO', 'EL', 'BA', 'ADP', 'CI', 'CL', 'SO', 'MRNA', 'LMT', 'TGT', 'ADI', 'GE', 'MDT', 'ABBV', 'WFC',
    'CVS', 'LRCX', 'WM', 'PGR', 'EW', 'ITW', 'CME', 'NEE', 'AON', 'FISV', 'TRV'
)

multi_select_dropdown = st.multiselect("Pick your assets", stocks)

start = st.date_input('Start', value = pd.to_datetime('2010-01-01'))
end = st.date_input('End', value = pd.to_datetime('today'))


def relative_return(df):
    relative_returns = df.pct_change()
    cumulative_return = (1 + relative_returns).cumprod() - 1
    cumulative_return = cumulative_return.fillna(0)
    return cumulative_return



if len(multi_select_dropdown) > 0:
    #df = yf.download(multi_select_dropdown, start, end)['Adj Close']
    df = relative_return(yf.download(multi_select_dropdown, start, end)['Adj Close'])
    st.write('Returns from stock {}'.format(multi_select_dropdown))
    st.line_chart(df)