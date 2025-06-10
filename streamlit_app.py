import streamlit as st
import yfinance as yf
import pandas as pd
from textblob import TextBlob
from datetime import datetime


def calculate_signal(df):
    """Return simple trading signal based on moving average crossover."""
    if len(df) < 200:
        return "Data not enough"
    df["SMA50"] = df["Close"].rolling(window=50).mean()
    df["SMA200"] = df["Close"].rolling(window=200).mean()
    if df["SMA50"].iloc[-1] > df["SMA200"].iloc[-1]:
        return "Bullish"
    return "Bearish"


def show_dashboard():
    st.header("Dashboard Pemantauan")
    st.write("Prestasi keseluruhan dan posisi terbuka akan dipaparkan di sini.")
    sample = pd.DataFrame({"PnL": [0, 1, 0.5, 2, 1.5]})
    st.line_chart(sample)


def show_scanner():
    st.header("Pengimbasan Pasaran AI")
    tickers = st.text_input("Senarai ticker (pisahkan dengan koma)", "AAPL,MSFT,GOOGL")
    if st.button("Imbas"):
        symbols = [t.strip() for t in tickers.split(",") if t.strip()]
        results = []
        for sym in symbols:
            df = yf.download(sym, period="1y")
            signal = calculate_signal(df)
            price = df["Close"].iloc[-1] if not df.empty else None
            results.append({"Ticker": sym, "Signal": signal, "Last Close": price})
        st.dataframe(pd.DataFrame(results))


def show_positions():
    st.header("Pengurusan Posisi")
    if "positions" not in st.session_state:
        st.session_state.positions = []
    if "history" not in st.session_state:
        st.session_state.history = []

    if st.session_state.positions:
        df = pd.DataFrame(st.session_state.positions)
        st.table(df)
    else:
        st.info("Tiada posisi dibuka")

    with st.form("open_position"):
        st.subheader("Buka Posisi Baru")
        ticker = st.text_input("Ticker")
        qty = st.number_input("Kuantiti", 1)
        submitted = st.form_submit_button("Buka")
        if submitted and ticker:
            price = yf.download(ticker, period="1d")['Close'].iloc[-1]
            st.session_state.positions.append({
                "ticker": ticker,
                "qty": qty,
                "entry": price,
                "opened": datetime.now().strftime("%Y-%m-%d")
            })
            st.success("Posisi dibuka")

    if st.session_state.positions:
        close_ticker = st.selectbox("Tutup posisi", [p["ticker"] for p in st.session_state.positions])
        if st.button("Tutup"):
            idx = next(i for i,p in enumerate(st.session_state.positions) if p["ticker"]==close_ticker)
            position = st.session_state.positions.pop(idx)
            last_price = yf.download(close_ticker, period="1d")['Close'].iloc[-1]
            profit = (last_price - position['entry']) * position['qty']
            position.update({"exit": last_price, "closed": datetime.now().strftime("%Y-%m-%d"), "pnl": profit})
            st.session_state.history.append(position)
            st.success(f"Posisi {close_ticker} ditutup. PnL: {profit:.2f}")


def show_technical():
    st.header("Analisis Teknikal")
    ticker = st.text_input("Ticker untuk dianalisis", "AAPL")
    if st.button("Analisis"):
        data = yf.download(ticker, period="1y")
        data["SMA50"] = data["Close"].rolling(window=50).mean()
        data["SMA200"] = data["Close"].rolling(window=200).mean()
        st.line_chart(data[["Close", "SMA50", "SMA200"]])
        st.write(calculate_signal(data))


def show_sentiment():
    st.header("Analisis Sentimen")
    text = st.text_area("Tajuk berita atau pernyataan")
    if st.button("Nilai Sentimen") and text:
        polarity = TextBlob(text).sentiment.polarity
        st.write(f"Polarity: {polarity}")


def show_performance():
    st.header("Laporan Prestasi")
    if "history" in st.session_state and st.session_state.history:
        history = pd.DataFrame(st.session_state.history)
        st.dataframe(history)
        cum_profit = history["pnl"].cumsum()
        st.line_chart(cum_profit)
    else:
        st.info("Belum ada dagangan diselesaikan.")


def show_settings():
    st.header("Tetapan Pengguna")
    risk = st.slider("Tahap risiko (%)", 1, 10, 2)
    st.session_state["risk"] = risk
    st.write(f"Risiko semasa: {risk}%")


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

