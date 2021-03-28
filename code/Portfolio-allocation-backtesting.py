import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd


weightings1 = {"SPY":"100"}
weightings2 = {"SPY":"95","BTC-USD":"5"}


members = ["BTC-USD","SPY"]


def PortfolioCalc(weightings, data, name):
  data[name] = sum([  int(weightings[x])*data[x]/100 for x in list(weightings.keys())   ])
  return data

basedata = yf.Ticker(members[0]).history(period="max").reset_index()[["Date","Open"]]
basedata["Date"] = pd.to_datetime(basedata["Date"])
basedata = basedata.rename(columns = {"Open":members[0]})


if (len(members)>1):
  for x in range(1,len(members)):
    newdata = yf.Ticker(members[x]).history(period="max").reset_index()[["Date","Open"]]
    newdata["Date"] = pd.to_datetime(newdata["Date"])
    newdata = newdata.rename(columns = {"Open":members[x]})
    basedata = pd.merge(basedata, newdata, on="Date")


basedata = basedata[  basedata["Date"] > "2016-01-01"]


print(basedata)

for x in members:
  basedata[x] = basedata[x]/(basedata[x].iloc[0])

basedata = PortfolioCalc(weightings1, basedata, "crypto1")
basedata = PortfolioCalc(weightings2, basedata, "crypto2")

#for x in members:
  #plt.semilogy(basedata["Date"], basedata[x], label=x)

plt.style.use("dark_background")

plt.plot(basedata["Date"], basedata["crypto1"], label = "100% s&p500")
plt.plot(basedata["Date"], basedata["crypto2"], label = "95% s&p500, 5% BTC")

plt.legend(loc="upper left")
plt.show()

















