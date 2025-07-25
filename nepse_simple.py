#!/bin/env python
# -*- coding: utf-8 -*-

import requests
import pandas as pd
import numpy as np
import openpyxl
import matplotlib.pyplot as plt
import bs4
import html5lib

asadas = """<html><head>NEPSE SIMPLE</head><header>
		
	<!-- Top header menu containing
		logo and Navigation bar -->
	<div id="top-header">
			
		<!-- Logo -->
		<div id="logo">
			<a href="https://sumityadav.com.np">
			<img src= https://rockerritesh.github.io/nepsesimple/android-chrome-192x192.png>	
			</a>	
		</div>
				
		<!-- Navigation Menu -->
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
	</div>
  <p><img class="lazyautosizes lazyloaded" src="https://github.com/rockerritesh/nepsesimple/raw/main/graph.png" data-src="https://github.com/rockerritesh/nepsesimple/raw/main/graph.png" data-srcset="https://github.com/rockerritesh/nepsesimple/raw/main/graph.png, https://github.com/rockerritesh/nepsesimple/raw/main/graph.png 1.5x, https://github.com/rockerritesh/nepsesimple/raw/main/graph.png 2x" data-sizes="auto" alt="https://github.com/rockerritesh/nepsesimple/raw/main/graph.png" title="Graph" sizes="800px" srcset="https://github.com/rockerritesh/nepsesimple/raw/main/graph.png, https://github.com/rockerritesh/nepsesimple/raw/main/graph.png 1.5x, https://github.com/rockerritesh/nepsesimple/raw/main/graph.png 2x"></p>
	<!-- Image menu in Header to contain an Image and
		a sample text over that image -->
	<div id="header-image-menu">

	</div>
</header>

<script button.addEventListener('click', () => {
  document.body.classList.toggle('dark')
  localStorage.setItem(
    'theme',
    document.body.classList.contains('dark') ? 'dark' : 'light'
  )
})
if (localStorage.getItem('theme') === 'dark') {
  document.body.classList.add('dark')
}></script>
     
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

<body>
"""

# --------- Fetch and process data from nepalstockinfo.com/stocklive (commented out as optional) ---------
"""
url = "https://nepalstockinfo.com/stocklive"
html = requests.get(url).content
df = pd.read_html(html)

df[0] = df[0].sort_values(by=["Previous Closing"])
df[0].pop("#")
df[0].pop("S.N.")

loc = "nepse_simple.xlsx"

df[0].to_csv("mydata.csv")
df[0].to_html("todaysummary.html")
df[0].to_excel(loc)

oxl = openpyxl.load_workbook(loc)
sheet = oxl.active

dims = {}
for row in sheet.rows:
    for cell in row:
        if cell.value:
            dims[cell.column_letter] = max(
                (dims.get(cell.column_letter, 0), len(str(cell.value)))
            )
for col, value in dims.items():
    sheet.column_dimensions[col].width = value

oxl.save(loc)
"""

# --------- Fetch and process Indices data with improved error handling ---------

url2 = "https://www.nepalipaisa.com/Indices.aspx"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/114.0.0.0 Safari/537.36"
}

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
        plot = data2[0 : data2.shape[0], 2]

        plt.figure(figsize=(40, 25))
        plt.plot(plot, "go--")
        plt.savefig("graph.png")
        print("Graph saved as graph.png")

    except Exception as e:
        print("Error parsing tables from Indices page:", e)
else:
    print("Failed to fetch Indices page")

# --------- Fetch and save stock data ---------
urlstock = "https://www.sharesansar.com/market"
htmlstock = requests.get(urlstock).content
df_list_stock = pd.read_html(htmlstock)
df_stock = df_list_stock[3]
df_stock.to_csv("stock.csv")
print("Stock data saved as stock.csv")

# --------- Fetch and save IPO data ---------
urlshare = "https://www.sharesansar.com/?show=home"
htmlshare = requests.get(urlshare).content
df_list_share = pd.read_html(htmlshare)
df_share = df_list_share[2]
df_share.to_csv("ipo.csv")
df_share.to_html("ipo.html")
print("IPO data saved as ipo.csv and ipo.html")

# --------- Fetch and save market summary pages ---------
nepse = requests.get("http://nepalstock.com")
soup = bs4.BeautifulSoup(nepse.text, "html5lib")
category = soup.find_all(class_="panel-body")

html = asadas + str(category[3]) + "</body> </html>"
with open("marketsummary.html", "w") as output:
    output.write(html)
print("marketsummary.html saved")

html = asadas + str(category[2]) + "</body> </html>"
with open("marketdata.html", "w") as output:
    output.write(html)
print("marketdata.html saved")

html = asadas + str(category[4]) + "</body> </html>"
with open("todayindex.html", "w") as output:
    output.write(html)
print("todayindex.html saved")

# --------- Fetch JSON from nepalstock.com today's price export ---------
df = pd.read_html("http://www.nepalstock.com/todaysprice/export")
df = df[-1].T
df.to_json("nepsesimple.json")
print("nepsesimple.json saved")

