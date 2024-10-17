
# **Stock Price Prediction and Analysis App**

## **Overview**

This project is a **Stock Price Prediction and Analysis App** built using **Streamlit** for the frontend, **Prophet** and **NeuralProphet** for time-series forecasting, **Yahoo Finance** for fetching stock data, and **Google News** for fetching the latest market-related news.

The app allows users to visualize stock data, predict future stock prices, and retrieve recent news headlines about selected stocks. It also provides a dashboard where users can compare multiple stocks and track their returns over a chosen time frame.

---

## **Features**

### 1. **Stock Data Visualization**
   - Allows users to select any stock from the S&P 100 list and view its historical stock data (Open, Close, High, Low, and Adjusted Close prices).
   - Visualizes stock data with interactive time-series graphs using Plotly.

### 2. **Stock Price Prediction**
   - Uses **Prophet** and **NeuralProphet** models for stock price prediction.
   - Users can select a stock and predict future prices for up to 4 years.
   - Displays forecast components such as trends and seasonality.

### 3. **Google News Stock Search**
   - Fetches and displays the latest news headlines related to the selected stock from Google News.
   - Users can keep track of the latest news and make better-informed stock predictions and decisions.

### 4. **Stock Dashboard**
   - A dashboard that allows users to select multiple stocks and compare their performance over a specific time period.
   - Displays the cumulative returns of the selected stocks in an easy-to-interpret line chart.

---

## **Technologies Used**

- **Frontend**: 
   - **Streamlit**: For creating the interactive web app interface.
   - **Plotly**: For generating dynamic and interactive visualizations.

- **Backend**: 
   - **yfinance**: To fetch real-time and historical stock data from Yahoo Finance.
   - **Prophet**: A time-series forecasting model developed by Facebook, for predicting stock prices.
   - **NeuralProphet**: An advanced neural network-based time-series forecasting model.
   - **Google News**: For fetching the latest stock-related news headlines.

---

## **Project Structure**

```
.
├── app
│   ├── tableau_dashboard.png        # Image for displaying Tableau dashboard
├── main.py                          # Main file to run the Streamlit app
├── google_news.py                   # File for fetching Google News
├── dashboard.py                     # Stock dashboard logic (merged into main.py)
└── README.md                        # This readme file
```

---

## **Usage**

- **Home**: Displays information about the app's features.
- **Visualization**: Allows users to select a stock and visualize its historical data with interactive charts.
- **Prediction**: Choose a stock and predict future prices using either Prophet or NeuralProphet models.
- **Google News**: Search for the latest news headlines related to the selected stock.
- **Dashboard**: Compare the performance of multiple stocks over a selected time range and view their cumulative returns.

---

## **Contributors**

- **Alessia Urzì** - Data Analyst
- **Sasha Crowe** - Data Analyst
- **Jean Philippe Auguste** - Data Analyst


