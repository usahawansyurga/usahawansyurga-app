import streamlit as st
import yfinance as yf
import pandas as pd
from textblob import TextBlob


def show_dashboard():
    st.header("Dashboard Pemantauan")
    st.write("Prestasi keseluruhan dan posisi terbuka akan dipaparkan di sini.")
    sample = pd.DataFrame({"PnL": [0, 1, 0.5, 2, 1.5]})
    st.line_chart(sample)


def show_scanner():
    st.header("Pengimbasan Pasaran AI")
    tickers = st.text_input("Senarai ticker (pisahkan dengan koma)", "AAPL,MSFT,GOOGL")
    if st.button("Imbas"):
        data = yf.download([t.strip() for t in tickers.split(",")], period="5d")
        st.write("Data harga terkini:")
        st.dataframe(data.tail())


def show_positions():
    st.header("Pengurusan Posisi")
    if "positions" not in st.session_state:
        st.session_state.positions = []

    st.write(pd.DataFrame(st.session_state.positions))

    with st.form("open_position"):
        st.subheader("Buka Posisi Baru")
        ticker = st.text_input("Ticker")
        qty = st.number_input("Kuantiti", 1)
        submitted = st.form_submit_button("Buka")
        if submitted and ticker:
            st.session_state.positions.append({"ticker": ticker, "qty": qty})
            st.success("Posisi dibuka")


def show_technical():
    st.header("Analisis Teknikal")
    ticker = st.text_input("Ticker untuk dianalisis", "AAPL")
    if st.button("Analisis"):
        data = yf.download(ticker, period="1y")
        data["SMA50"] = data["Close"].rolling(window=50).mean()
        data["SMA200"] = data["Close"].rolling(window=200).mean()
        st.line_chart(data[["Close", "SMA50", "SMA200"]])


def show_sentiment():
    st.header("Analisis Sentimen")
    text = st.text_area("Tajuk berita atau pernyataan")
    if st.button("Nilai Sentimen") and text:
        polarity = TextBlob(text).sentiment.polarity
        st.write(f"Polarity: {polarity}")


def show_performance():
    st.header("Laporan Prestasi")
    st.write("Carta prestasi dagangan contoh di bawah.")
    sample = pd.DataFrame({"Keuntungan": [0, 1, 1.5, 2, 3]})
    st.area_chart(sample)


def show_settings():
    st.header("Tetapan Pengguna")
    st.write("Laraskan parameter dagangan dan API di sini.")


pages = {
    "Dashboard": show_dashboard,
    "Pengimbasan": show_scanner,
    "Posisi": show_positions,
    "Analisis Teknikal": show_technical,
    "Analisis Sentimen": show_sentiment,
    "Laporan": show_performance,
    "Tetapan": show_settings,
}

choice = st.sidebar.selectbox("Menu", list(pages.keys()))
pages[choice]()

