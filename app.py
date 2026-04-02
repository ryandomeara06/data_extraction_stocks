import streamlit as st 
import yfinance as yf 
import pandas as pd 
import matplotlib.pyplot as plt


st.set_page_config(page_title = "Stock Data Extraction", layout="wide")

st.title ("Stock Data Extraction App")

st.write("Extract stock market prices from yahoo finance using ticker")


st.sidebar.header("User input")

ticker = st.sidebar.text_input("Enter Ticker", "AAPL")

start_date = st.sidebar.date_input("start date", pd.to_datetime("2023-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("today"))

# download the data
if st.sidebar.button("Get Data"):

  # create ticker object 
  stock = yf.ticker(ticker)

  #  download historical prices 
  df = stock.history(start = start_date, end = end_date)

  # check the data
  if df.empty:
    st.error("Not Data Found. Pleach check the ticker symbol or date range")
  else:
    st.success(f"Data Succesfully extracted for {ticker}")

    # display company info
    st.subheader("Company Information")
    info = stock.info


    company_name = info.get("LongName", "N/A")
    sector = info.get("sector", "N/A")
    industry = info.get("industry", "N/A")
    market_cap = info.get("marketcap", "N/A")
    website = info.get("website", "N/A")


    st.write(f"**Company Name:** {company_name}")
    st.write(f"**Sector:** {sector}")

    st.subheader("Historical data")
    st.dataframe(df)

    st.subheader("closing price chart")
    fig, ax = plt.subplots()
    ax.plot(df.index, df['Close'])
    ax.set_xlabel("Date")
    ax.set_ylabel("Closing Price")
    st.pyplot(fig)


    # convert dataframe to CSV for download 
    csv = df.to_csv().encode("utf-8")

    #  create download button for CSV

  st.download_button(
      label = "Download Data as CSV"
      data = csv
      file_name = f"{ticker}_stock_data.csv"
      mime = "text/csv"
  )
