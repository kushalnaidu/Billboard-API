# -*- coding: utf-8 -*-
"""
Created on Tue Jul 17 11:33:34 2018

@author: Kushal
"""
import certifi
import urllib3
from bs4 import BeautifulSoup
from datetime import datetime
from datetime import timedelta
position = 1
url = "https://www.billboard.com/charts/hot-100/2018-07-10"
http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())
r = http.request('GET', url)
soup = BeautifulSoup(r.data, "lxml")
attribute_class = 'chart-details'
article = soup.find('div', attrs = {'class':attribute_class})
song = article.find('div', attrs = {'data-rank':str(55)})
print(song.attrs)

