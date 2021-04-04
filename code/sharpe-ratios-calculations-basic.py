import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

timeperiod=365

df = yf.Ticker("BTC-USD").history(period="max").reset_index()[["Date","Open"]]

df = df.rename(columns = {"Open":"btc"})
df["Date"] = pd.to_datetime(df["Date"])

xmrdata = yf.Ticker("XMR-USD").history(period="max").reset_index()[["Date","Open"]]
xmrdata = xmrdata.rename(columns = {"Open":"xmr"})
xmrdata["Date"] = pd.to_datetime(xmrdata["Date"])

df = df.merge(xmrdata, on="Date", how="left")

df["btcret"] = 100 *(df["btc"]/df["btc"].shift(timeperiod) -1)
df["xmrret"] = 100 *(df["xmr"]/df["xmr"].shift(timeperiod) -1)

df["btcstd"] = df["btcret"].rolling(timeperiod).std()
df["xmrstd"] = df["xmrret"].rolling(timeperiod).std()

df["btcsharpe"] = df["btcret"]/df["btcstd"]
df["xmrsharpe"] = df["xmrret"]/df["xmrstd"]

plt.style.use("dark_background")

plt.plot(df["Date"],df["btcsharpe"], label="BTC")
plt.plot(df["Date"],df["xmrsharpe"], label="XMR")
#plt.plot(df["Date"],df["xmrsharpe"] - df["btcsharpe"], label="XMR - BTC")
plt.title("Sharpe Ratios of BTC and XMR", size = 20)
plt.legend()
plt.show()


