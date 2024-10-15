import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import date
from prophet import Prophet
from neuralprophet import NeuralProphet
from plotly import graph_objs as go
from prophet.plot import plot_plotly 


# Set page layout
st.set_page_config(layout="wide")

START = "2010-01-01"
TODAY = date.today().strftime("%Y-%m-%d")
stocks = (
    'AAPL', 'MSFT', 'AMZN', 'GOOGL', 'GOOG', 'FB', 'BRK.B', 'JNJ', 'NVDA', 'JPM', 'UNH', 'V', 'PG', 'HD',
    'MA', 'PFE', 'BAC', 'DIS', 'VZ', 'KO', 'NFLX', 'INTC', 'MRK', 'CSCO', 'T', 'CMCSA', 'CVX', 'XOM', 'PEP', 'ABT',
    'ADBE', 'WMT', 'NKE', 'PYPL', 'TMO', 'CRM', 'ORCL', 'MCD', 'MDT', 'COST', 'AXP', 'LLY', 'BMY', 'QCOM',
    'DHR', 'TXN', 'UNP', 'UPS', 'LIN', 'SBUX', 'HON', 'AVGO', 'AMGN', 'CAT', 'AMT', 'GILD', 'GS', 'SCHW',
    'BKNG', 'MS', 'ISRG', 'SPGI', 'ZTS', 'INTU', 'FIS', 'USB', 'RTX', 'DE', 'C', 'BLK', 'PLD', 'MMM', 'IBM', 'NOW',
    'SYK', 'CB', 'MO', 'EL', 'BA', 'ADP', 'CI', 'CL', 'SO', 'MRNA', 'LMT', 'TGT', 'ADI', 'GE', 'MDT', 'ABBV', 'WFC',
    'CVS', 'LRCX', 'WM', 'PGR', 'EW', 'ITW', 'CME', 'NEE', 'AON', 'FISV', 'TRV'
)

@st.cache_data
def load_data(ticker):
    data = yf.download(ticker, START, TODAY)
    data.reset_index(inplace=True)
    return data

# Function to plot raw data
def plot_raw_data(data):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name='Stock_close'))
    fig.layout.update(title_text='Time Series Data', xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)

# Main app function
def main():
    st.title("Stock Prediction App")
    
    # User choice for prediction model
    choice = st.sidebar.selectbox("Choose Prediction Model", ('Predict with Prophet', 'Predict with NeuralProphet'))

    selected_stocks = st.selectbox("Select dataset for prediction", stocks)

    n_years = st.slider("Years of prediction:", 1, 4)
    period = n_years * 365

    data_load_state = st.text("Loading data...")
    data = load_data(selected_stocks)
    data_load_state.text("Loading data ... DONE!")

    st.subheader("Raw data")
    st.write(data.tail())

    plot_raw_data(data)

    if choice == 'Predict with Prophet':
        st.subheader("Prophet Model")
        df_train = data[['Date', 'Close']]
        df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

        # Prophet model fitting
        m = Prophet()
        m.fit(df_train)

        # Make future predictions
        future = m.make_future_dataframe(periods=period)
        forecast = m.predict(future)

        st.subheader("Forecast data")
        st.write(forecast.tail())

        # Plot forecast data using Prophet's plot
        fig1 = plot_plotly(m, forecast)
        st.plotly_chart(fig1)


        st.write("Forecast component")
        fig2 = m.plot_components(forecast)
        st.write(fig2)

    elif choice == "Predict with NeuralProphet":
        st.subheader("NeuralProphet Model")
        df_train = data[['Date', 'Close']]
        df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

        # NeuralProphet model fitting
        m = NeuralProphet()
        m.fit(df_train, freq="D")

        # Make future predictions with NeuralProphet
        future = m.make_future_dataframe(df=df_train, n_historic_predictions=True, periods=period)
        forecast = m.predict(future)

        st.subheader("Forecast data")
        st.write(forecast.tail())

        # Plot forecast data using NeuralProphet's plot
        fig1 = m.plot(forecast)
        st.write(fig1)

        # Plot forecast components
        st.write("Forecast component")
        fig2 = m.plot_components(forecast)
        st.write(fig2)

if __name__ == '__main__':
    main()