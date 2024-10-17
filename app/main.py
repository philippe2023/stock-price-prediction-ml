import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import yfinance as yf
from datetime import date
from prophet import Prophet
from neuralprophet import NeuralProphet
from plotly import graph_objs as go
from prophet.plot import plot_plotly
from GoogleNews import GoogleNews 

# Set page layout
st.set_page_config(layout="wide")

# Constants
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

# Function to get news headlines using GoogleNews
def get_titles(search):
    googlenews = GoogleNews(lang='en')
    googlenews.search(search)
    result = googlenews.result()

    stories = []
    for item in result:
        story = {
            'title': item['title'],
            'link': item['link']
        }
        stories.append(story)

    return stories

# Google News Page logic
def google_news_page():
    st.title("Google News Stock Search")

    # Stock selector for news
    selected_stock = st.selectbox("Select stock for news", stocks)
    st.subheader(f"Latest Google News for {selected_stock}")

    # Button to trigger news search
    if st.button("Fetch News"):
        st.write(f"Fetching news headlines for {selected_stock}...")

        # Fetch news headlines from Google News
        headlines = get_titles(selected_stock)

        if headlines:
            st.success("News fetched successfully!")
            for i, headline in enumerate(headlines, 1):
                st.markdown(f"{i}. [{headline['title']}]({headline['link']})")
        else:
            st.warning(f"No news headlines found for {selected_stock}.")

# Dashboard Page logic
def dashboard_page():
    st.title("My Stock Dashboard")

    # Stock selector for the dashboard
    multi_select_dropdown = st.multiselect("Pick your assets", stocks)

    # Date input fields for the dashboard
    start = st.date_input('Start', value=pd.to_datetime('2010-01-01'))
    end = st.date_input('End', value=pd.to_datetime('today'))

    # Function to calculate relative return
    def relative_return(df):
        relative_returns = df.pct_change()
        cumulative_return = (1 + relative_returns).cumprod() - 1
        cumulative_return = cumulative_return.fillna(0)
        return cumulative_return

    # Only show chart if stocks are selected
    if len(multi_select_dropdown) > 0:
        # Download stock data and calculate relative returns
        df = relative_return(yf.download(multi_select_dropdown, start, end)['Adj Close'])
        st.write(f'Returns for stocks: {multi_select_dropdown}')
        st.line_chart(df)

# Main app function
def main():
    # Sidebar for navigation
    st.sidebar.title("Stock App")
    page = st.sidebar.radio("Go to", ["Home", "Visualization", "Prediction", "Google News", "Dashboard"])  # Added Dashboard

    # Home Page
    if page == "Home":
        st.title("Welcome to the Stock Prediction App")
        st.write("""
        This app allows you to predict stock prices using two models: **Prophet** and **NeuralProphet**.

        ### Features:
        - **Visualization**: Explore raw stock data with interactive visualizations.
        - **Prophet**: Time-series forecasting developed by Facebook.
        - **NeuralProphet**: Neural network-based time-series forecasting.
        - **Market News**: Get up-to-date news on your desired stock.
        - **Personal Dashboard**: Compare your preferred stocks.
        """)
    
    # Visualization Page
    elif page == "Visualization":
        st.title("Stock Data Visualization")
        selected_stocks = st.selectbox("Select dataset for visualization", stocks)

        data_load_state = st.text("Loading data...")
        data = load_data(selected_stocks)
        data_load_state.text("Loading data ... DONE!")

        st.subheader("Raw data")
        st.write(data.tail())

        # Plot raw data
        plot_raw_data(data)
        
        # Tableau Visuals
        st.subheader("Stock Price Dashboard Visualization")
        image = Image.open("app/tableau_dashboard.png")
        st.image(image, caption="Stock Price Tableau Dashboard", use_column_width=False, width=800)
        st.markdown("""
        **[Click here to view the Tableau Dashboard](https://public.tableau.com/views/Stock-price-predictor-ml/Dashboard1?:language=en-GB&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)**  
        Please note that this will open the dashboard in a new tab.
        """)
        
    # Prediction Page
    elif page == "Prediction":
        st.title("Stock Prediction")

        # User choice for prediction model
        choice = st.sidebar.selectbox("Choose Prediction Model", ('Predict with Prophet', 'Predict with NeuralProphet'))

        selected_stocks = st.selectbox("Select dataset for prediction", stocks)

        n_years = st.slider("Years of prediction:", 0, 4)
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
            m = NeuralProphet(
            yearly_seasonality=10,   # Control how much yearly seasonality to use
            weekly_seasonality=False # Disable weekly seasonality if it's causing noise
            )

            m.fit(df_train, freq="D")  # Daily frequency

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

    # Google News Page
    elif page == "Google News":
        google_news_page()  # Call the Google News page
    
    # Dashboard Page
    elif page == "Dashboard":
        dashboard_page()  # Call the Dashboard page

if __name__ == '__main__':
    main()