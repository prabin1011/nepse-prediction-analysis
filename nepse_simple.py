#!/bin/env python
# -*- coding: utf-8 -*-

import requests
import pandas as pd
import numpy as np
import openpyxl
import matplotlib.pyplot as plt
import bs4
import html5lib

# --------- Fetch and save stock live data (optional, uncomment to enable) ---------
"""
try:
    url = "https://nepalstockinfo.com/stocklive"
    html = requests.get(url).content
    df = pd.read_html(html)

    df[0] = df[0].sort_values(by=["Previous Closing"])
    df[0].pop("#")
    df[0].pop("S.N.")

    loc = "nepse_simple.xlsx"

    df[0].to_csv("mydata.csv", encoding='utf-8')
    df[0].to_html("todaysummary.html", encoding='utf-8')
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
    print("Stock live data saved to mydata.csv, todaysummary.html, and nepse_simple.xlsx")
except Exception as e:
    print("Error in stock live data section:", e)
"""

# --------- Fetch and process Indices data with error handling ---------
url2 = "https://www.nepalipaisa.com/Indices.aspx"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/114.0.0.0 Safari/537.36"
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

    html_market_summary = "<html><head><title>Market Summary</title></head><body>" + str(category[3]) + "</body></html>"
    with open("marketsummary.html", "w", encoding='utf-8') as output:
        output.write(html_market_summary)
    print("marketsummary.html saved")

    html_market_data = "<html><head><title>Market Data</title></head><body>" + str(category[2]) + "</body></html>"
    with open("marketdata.html", "w", encoding='utf-8') as output:
        output.write(html_market_data)
    print("marketdata.html saved")

    html_today_index = "<html><head><title>Today Index</title></head><body>" + str(category[4]) + "</body></html>"
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
