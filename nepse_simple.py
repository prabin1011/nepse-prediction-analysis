#!/bin/env python
# -*- coding: utf-8 -*-

import requests
import pandas as pd
import numpy as np
import openpyxl
import matplotlib.pyplot as plt
import bs4
import html5lib

# HTML template header (asadas)
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
