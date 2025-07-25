#!/bin/env python
# -*- coding: utf-8 -*-

import requests
import pandas as pd
import numpy as np
import openpyxl
import matplotlib.pyplot as plt
import bs4
import html5lib

# Corrected asadas with proper HTML structure
asadas = """<html>
<head>
  <title>NEPSE SIMPLE</title>
  <script>
  document.getElementById('mode-toggle').addEventListener('click', () => {
    document.body.classList.toggle('dark')
    localStorage.setItem(
      'theme',
      document.body.classList.contains('dark') ? 'dark' : 'light'
    )
  })
  if (localStorage.getItem('theme') === 'dark') {
    document.body.classList.add('dark')
  }
  </script>
  <style>
    body{
      padding:10% 3% 10% 3%;
      text-align:center;
    }
    img{
      height:140px;
      width:140px;
    }
    h1{
      color: #32a852;
    }
    .mode {
      float:right;
    }
    .change {
      cursor: pointer;
      border: 1px solid #555;
      border-radius: 40%;
      width: 20px;
      text-align: center;
      padding: 5px;
      margin-left: 8px;
    }
    .dark{
      background-color: #000;
      color: #fff;
    }
  </style>
</head>
<body>
  <header>
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
          <p dir="auto"><a href="https://github.com/rockerritesh/nepsesimple/actions/workflows/update.yml"><img src="https://github.com/rockerritesh/nepsesimple/actions/workflows/update.yml/badge.svg" alt="Update file(s)" style="max-width: 100%;"></a></p>
        </ul>
      </nav>
      <button id="mode-toggle">Toggle Dark Mode</button>
    </div>
    <p><img class="lazyautosizes lazyloaded" src="https://github.com/rockerritesh/nepsesimple/raw/main/graph.png" data-src="https://github.com/rockerritesh/nepsesimple/raw/main/graph.png" data-srcset="https://github.com/rockerritesh/nepsesimple/raw/main/graph.png, https://github.com/rockerritesh/nepsesimple/raw/main/graph.png 1.5x, https://github.com/rockerritesh/nepsesimple/raw/main/graph.png 2x" data-sizes="auto" alt="https://github.com/rockerritesh/nepsesimple/raw/main/graph.png" title="Graph" sizes="800px" srcset="https://github.com/rockerritesh/nepsesimple/raw/main/graph.png, https://github.com/rockerritesh/nepsesimple/raw/main/graph.png 1.5x, https://github.com/rockerritesh/nepsesimple/raw/main/graph.png 2x"></p>
    <div id="header-image-menu">
    </div>
  </header>
  <!-- main content will be added here -->
"""

# Rest of your code remains unchanged
# ... (include all other parts of your code here)

# For example:
# --------- Fetch and process Indices data with error handling ---------
url2 = "https://www.nepalipaisa.com/Indices.aspx"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

try:
    response = requests.get(url2, headers=headers)
    print("Status code for Indices:", response.status_code)

    if response.status_code == 200:
        html2 = response.content
        try:
            df_list2 = pd.read_html(html2)
            print(f"Found {len(df_list2)} tables in Indices page")
            df22 = df_list2[-1]

            data2 = np.array(df22)
            data2 = np.flip(data2)
            plot = data2[0: data2.shape[0], 2]

            plt.figure(figsize=(40, 25))
            plt.plot(plot, "go--")
            plt.savefig("graph.png")
            plt.close()
            print("Graph saved as graph.png")
        except Exception as e:
            print("Error parsing tables from Indices page:", e)
    else:
        print("Failed to fetch Indices page")
except Exception as e:
    print("Error fetching Indices page:", e)

# --------- Fetch and save stock data ---------
try:
    urlstock = "https://www.sharesansar.com/market"
    htmlstock = requests.get(urlstock).content
    df_list_stock = pd.read_html(htmlstock)
    df_stock = df_list_stock[3]
    df_stock.to_csv("stock.csv", encoding='utf-8')
    print("Stock data saved as stock.csv")
except Exception as e:
    print("Error in stock data section:", e)

# --------- Fetch and save IPO data ---------
try:
    urlshare = "https://www.sharesansar.com/?show=home"
    htmlshare = requests.get(urlshare).content
    df_list_share = pd.read_html(htmlshare)
    df_share = df_list_share[2]
    df_share.to_csv("ipo.csv", encoding='utf-8')
    df_share.to_html("ipo.html", encoding='utf-8')
    print("IPO data saved as ipo.csv and ipo.html")
except Exception as e:
    print("Error in IPO data section:", e)

# --------- Fetch and save market summary pages ---------
try:
    nepse = requests.get("http://nepalstock.com")
    soup = bs4.BeautifulSoup(nepse.text, "html5lib")
    category = soup.find_all(class_="panel-body")

    html_market_summary = asadas + str(category[3]) + "</body></html>"
    with open("marketsummary.html", "w", encoding='utf-8') as output:
        output.write(html_market_summary)
    print("marketsummary.html saved")

    html_market_data = asadas + str(category[2]) + "</body></html>"
    with open("marketdata.html", "w", encoding='utf-8') as output:
        output.write(html_market_data)
    print("marketdata.html saved")

    html_today_index = asadas + str(category[4]) + "</body></html>"
    with open("todayindex.html", "w", encoding='utf-8') as output:
        output.write(html_today_index)
    print("todayindex.html saved")
except Exception as e:
    print("Error in market summary section:", e)

# --------- Fetch JSON from nepalstock.com today's price export ---------
try:
    df = pd.read_html("http://www.nepalstock.com/todaysprice/export")
    df = df[-1].T
    df.to_json("nepsesimple.json", orient='columns', force_ascii=False)
    print("nepsesimple.json saved")
except Exception as e:
    print("Error in JSON export section:", e)
