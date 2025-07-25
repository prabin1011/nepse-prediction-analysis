# /bin/env python
# -*- coding: utf-8 -*-

import requests
import pandas as pd
import numpy as np
import openpyxl
import matplotlib.pyplot as plt
import bs4
import html5lib

# HTML Template
asadas = """
<html><head><title>NEPSE SIMPLE</title></head><header>
<div id="top-header">
  <div id="logo">
    <a href="https://sumityadav.com.np">
      <img src="https://rockerritesh.github.io/nepsesimple/android-chrome-192x192.png">	
    </a>	
  </div>
  <nav>
    <ul>
      <li class="active"><a href="https://rockerritesh.github.io/nepsesimple/index">Home</a></li>
      <li><a href="https://rockerritesh.github.io/nepsesimple/todaysummary">Today Summary</a></li> 
      <li><a href="https://rockerritesh.github.io/nepsesimple/marketsummary">Summary</a></li>
      <li><a href="https://rockerritesh.github.io/nepsesimple/marketdata">Top Value Data</a></li>
      <li><a href="https://rockerritesh.github.io/nepsesimple/ipo">IPO</a></li>
      <li><a href="https://rockerritesh.github.io/nepsesimple/todayindex">Indices</a></li>
      <li><a href="https://rockerritesh.github.io/nepsesimple/each_company">Each Company</a></li>
    </ul>
  </nav>
</div>
<p><img src="https://github.com/rockerritesh/nepsesimple/raw/main/graph.png" width="800"></p>
<style>
  body {
    padding:10% 3% 10% 3%;
    text-align:center;
  }
  img {
    height:140px;
    width:140px;
  }
  h1 {
    color: #32a852;
  }
  .dark {
    background-color: #000;
    color: #fff;
  }
</style>
</header><body>
"""

# ==== DATA COLLECTION & FILE GENERATION ====

# 1. Generate NEPSE Index Graph
url2 = "https://www.nepalipaisa.com/Indices.aspx"
html2 = requests.get(url2).content
df_list2 = pd.read_html(html2)
df22 = df_list2[-1]

data2 = np.flip(np.array(df22))
plot = data2[:, 2]

plt.figure(figsize=(40, 25))
plt.plot(plot, "go--")
plt.savefig("graph.png")

# 2. Market Summary / Top Value / Today Index
nepse = requests.get("http://nepalstock.com")
soup = bs4.BeautifulSoup(nepse.text, "html5lib")
category = soup.find_all(class_="panel-body")

with open("marketsummary.html", "w") as f:
    f.write(asadas + str(category[3]) + "</body></html>")

with open("marketdata.html", "w") as f:
    f.write(asadas + str(category[2]) + "</body></html>")

with open("todayindex.html", "w") as f:
    f.write(asadas + str(category[4]) + "</body></html>")

# 3. Stock Data (Table 3)
urlstock = "https://www.sharesansar.com/market"
df_stock = pd.read_html(requests.get(urlstock).content)[3]
df_stock.to_csv("stock.csv")

# 4. IPO Data (Table 2)
urlshare = "https://www.sharesansar.com/?show=home"
df_share = pd.read_html(requests.get(urlshare).content)[2]
df_share.to_csv("ipo.csv")
df_share.to_html("ipo.html")

# 5. All Company Listing (JSON for API)
df_nepse = pd.read_html("http://www.nepalstock.com/todaysprice/export")[-1].T
df_nepse.to_json("nepsesimple.json")

# 6. Optional - Each Company (dummy placeholder)
# dfall = pd.read_json("https://nepalstock-api.herokuapp.com/nepse-index")
# html = asadas + dfall.to_html() + "</body></html>"
# with open("each_company.html", "w") as f:
#     f.write(html)

