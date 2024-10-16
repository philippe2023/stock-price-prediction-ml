import streamlit as st
from GoogleNews import GoogleNews

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

# Streamlit App Layout
def main():
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

if __name__ == '__main__':
    main()