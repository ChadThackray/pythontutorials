import plotly.express as px
import re
import requests
import pandas as pd
import json
import numpy as np

subs = pd.read_csv("subreddits.csv")

gecko = list(subs["gecko-name"])
subreddits = list(subs["reddit"])
subSize = []
mktcap = []

for x in subreddits:
  data = requests.get("https://frontpagemetrics.com/r/" + x).text
  data = re.findall("h2 class=.*",data)
  data = re.findall(">[0-9,]*<",data[0])[0]
  data = data.replace(">","").replace("<","").replace(",","")
  subSize.append(int(data))

subs["size"] = subSize

for x in gecko:
  data = requests.get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=" + x +"&order=market_cap_desc&per_page=100&page=1&sparkline=false")
  mktcap.append(int(data.json()[0]["market_cap"]))

subs["mktcap"] = mktcap
subs["kvalue"] = subs["mktcap"]/(subs["size"]**2)

fig = px.scatter(subs, x="size", y="mktcap",
	         size="kvalue",
                 hover_name="gecko-name", text = "gecko-name",template="plotly_dark",log_x=True,log_y=True,size_max=200)

fig.update_xaxes(title_text='Reddit Subscribers',
                 showgrid=False,
                 title_font = {"size": 30})
fig.update_yaxes(title_text='<br>Marketcap',
                 showgrid=False,
                 title_font = {"size": 30})

fig.update_layout(title_text="Relative valuations by Metcalfe's law", 
                  title_font_size=45,
                  title_yanchor="top",
                  title_pad_t=30,
                  title_pad_b=30)

fig.show()





