import pandas as pd
import numpy as np
import yfinance as yf
import plotly as pt
import streamlit as st
from datetime import date
from prophet import Prophet
from neuralprophet import NeuralProphet
from plotly import graph_objs as go

START = "2010-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

st.title("Stock Prediction App")

stocks = (
    'AAPL', 'MSFT', 'AMZN', 'GOOGL', 'GOOG', 'FB', 'BRK.B', 'JNJ', 'NVDA', 'JPM', 'UNH', 'V', 'PG', 'HD',
    'MA', 'PFE', 'BAC', 'DIS', 'VZ', 'KO', 'NFLX', 'INTC', 'MRK', 'CSCO', 'T', 'CMCSA', 'CVX', 'XOM', 'PEP', 'ABT',
    'ADBE', 'WMT', 'NKE', 'PYPL', 'TMO', 'CRM', 'ORCL', 'MCD', 'MDT', 'COST', 'AXP', 'LLY', 'BMY', 'QCOM',
    'DHR', 'TXN', 'UNP', 'UPS', 'LIN', 'SBUX', 'HON', 'AVGO', 'AMGN', 'CAT', 'AMT', 'GILD', 'GS', 'SCHW',
    'BKNG', 'MS', 'ISRG', 'SPGI', 'ZTS', 'INTU', 'FIS', 'USB', 'RTX', 'DE', 'C', 'BLK', 'PLD', 'MMM', 'IBM', 'NOW',
    'SYK', 'CB', 'MO', 'EL', 'BA', 'ADP', 'CI', 'CL', 'SO', 'MRNA', 'LMT', 'TGT', 'ADI', 'GE', 'MDT', 'ABBV', 'WFC',
    'CVS', 'LRCX', 'WM', 'PGR', 'EW', 'ITW', 'CME', 'NEE', 'AON', 'FISV', 'TRV'
)

selected_stocks = st.selectbox("Select dataset for prediction", stocks)

n_years = st.slider("Years of prediction:", 0, 4)
period = n_years * 365

@st.cache_data
def load_data(ticker):
    data = yf.download(ticker, START, TODAY)
    data.reset_index(inplace=True)
    return data

data_load_state = st.text("Load data...")
data = load_data(selected_stocks)
data_load_state.text("Loading data ... DONE!")

st.subheader("Raw data")
st.write(data.tail())

def plot_raw_data():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name='Stock_close'))
    fig.layout.update(title_text='Time Series Data', xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)

plot_raw_data()

# Forecasting with NeuralProphet
df_train = data[['Date', 'Close']]
df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

m = NeuralProphet()
m.fit(df_train, freq="D")

future = m.make_future_dataframe(df=df_train, n_historic_predictions=True, periods=period)
forecast = m.predict(future)

st.subheader("Forecast data")
st.write(forecast.tail())

# Use NeuralProphet's native plotting
st.write("Forecast data")
fig1 = m.plot(forecast)  # Corrected plotting method for NeuralProphet
st.write(fig1)

st.write("Forecast component")
fig2 = m.plot_components(forecast)
st.write(fig2)