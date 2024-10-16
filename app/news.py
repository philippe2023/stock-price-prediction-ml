import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Stock tickers (you can add more tickers to this list)
stocks = (
    'AAPL', 'MSFT', 'AMZN', 'GOOGL', 'GOOG', 'FB', 'BRK.B', 'JNJ', 'NVDA', 'JPM', 'UNH', 'V', 'PG', 'HD',
    'MA', 'PFE', 'BAC', 'DIS', 'VZ', 'KO', 'NFLX', 'INTC', 'MRK', 'CSCO', 'T', 'CMCSA', 'CVX', 'XOM', 'PEP', 'ABT',
    'ADBE', 'WMT', 'NKE', 'PYPL', 'TMO', 'CRM', 'ORCL', 'MCD', 'MDT', 'COST', 'AXP', 'LLY', 'BMY', 'QCOM',
    'DHR', 'TXN', 'UNP', 'UPS', 'LIN', 'SBUX', 'HON', 'AVGO', 'AMGN', 'CAT', 'AMT', 'GILD', 'GS', 'SCHW',
    'BKNG', 'MS', 'ISRG', 'SPGI', 'ZTS', 'INTU', 'FIS', 'USB', 'RTX', 'DE', 'C', 'BLK', 'PLD', 'MMM', 'IBM', 'NOW',
    'SYK', 'CB', 'MO', 'EL', 'BA', 'ADP', 'CI', 'CL', 'SO', 'MRNA', 'LMT', 'TGT', 'ADI', 'GE', 'MDT', 'ABBV', 'WFC',
    'CVS', 'LRCX', 'WM', 'PGR', 'EW', 'ITW', 'CME', 'NEE', 'AON', 'FISV', 'TRV'
)

# Function to get the Yahoo Finance page and return the parsed HTML document
def get_page(url):
    response = requests.get(url)
    if not response.ok:
        st.error(f"Failed to load page {url}. Status code: {response.status_code}")
        return None
    page_content = response.text
    doc = BeautifulSoup(page_content, 'html.parser')
    return doc

# Function to scrape general news and filter it based on stock ticker
def scrape_news(stock):
    # General Yahoo Finance news page
    my_url = "https://finance.yahoo.com/topic/stock-market-news/"
    doc = get_page(my_url)
    
    if doc is None:
        return []

    # Find the relevant tags containing news headlines
    a_tags = doc.find_all('a', {'class': "js-content-viewer"})

    news_list = []
    for tag in a_tags:
        headline = tag.text.strip()  # Strip any extra spaces
        # Check if the stock ticker is mentioned in the headline
        if stock in headline:
            link = "https://finance.yahoo.com" + tag['href']
            news_list.append(f"{headline} - [Link]({link})")
    
    return news_list

# New function to scrape headlines from Yahoo Finance's stock market news page
def get_headlines():
    my_url = 'https://finance.yahoo.com/topic/stock-market-news/'
    doc = get_page(my_url)

    if doc is None:
        return pd.DataFrame()  # Return an empty DataFrame in case of failure

    news_list = []
    for e in doc.select('div:has(>h3>a)'):
        news = e.h3.text
        news_list.append(news)

    news_df = pd.DataFrame(news_list, columns=["Headline"])
    return news_df

# Streamlit App Layout
def main():
    st.title("Stock News Scraper")
    
    # Stock selector for news
    selected_stocks = st.selectbox("Select stock for news", stocks)
    st.subheader(f"Latest News for {selected_stocks}")
    
    # Button to trigger scraping for stock-specific news
    if st.button("Fetch Stock-Specific News"):
        st.write(f"Fetching news headlines mentioning {selected_stocks}...")
        
        # Scrape the news headlines that mention the selected stock
        headlines = scrape_news(selected_stocks)
        
        if headlines:
            st.success("News fetched successfully!")
            for i, headline in enumerate(headlines, 1):
                st.markdown(f"{i}. {headline}")
        else:
            st.warning(f"No news headlines mentioning {selected_stocks} found.")
    
    st.write("Note: This app fetches the latest financial headlines and filters those mentioning the selected stock from Yahoo Finance.")
    
    st.subheader("General Stock Market News")
    
    # Button to trigger scraping of general stock market news
    if st.button("Fetch General News"):
        st.write("Fetching general stock market news...")
        
        news_df = get_headlines()
        
        if not news_df.empty:
            st.success("General stock market news fetched successfully!")
            st.dataframe(news_df)  # Display the DataFrame in Streamlit
        else:
            st.warning("No general stock market news found.")

if __name__ == '__main__':
    main()