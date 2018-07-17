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
def validate_date(date):
    date = date.split('-')
    if len(date[1]) is not 2:
        date[1] = '0'+date[1]
    if len(date[2]) is not 2:
        date[2] = '0'+date[2]
        date = '-'.join(date)
    try:
        datetime.strptime(date, '%Y-%m-%d')
        return date;
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")

def data_extractor(soup, position):
    if position is not 1 :
        attribute_class = 'chart-details'
        article = soup.find('div', attrs = {'class':attribute_class})
        song = article.find('div', attrs = {'data-rank':str(position)})
        song_name = song.attrs['data-title']
        artist_name = song.attrs['data-artist']
        print(song_name)
        print(artist_name)
    else:
        attribute_class = 'chart-number-one__info'
        article = soup.find('div', attrs = {'class':attribute_class})
        song = article.find('div', attrs = {'class':'chart-number-one__title'})
        artist = article.find('div', attrs = {'class':'chart-number-one__artist'})
        print(song.text.strip())
        print(artist.text.strip())
        
def scraper(date = str(datetime.today()-timedelta(days=7)).split()[0], position = None, start_position = 1, end_position = 100):
    
    
    first_date = datetime(1958,8,4)
    date = validate_date(date)
    if datetime.strptime(date, '%Y-%m-%d') < first_date:
        date = str(first_date).split()[0]
    if datetime.strptime(date, '%Y-%m-%d') > datetime.today()-timedelta(days = 7):
        date = str(datetime.today()-timedelta(days=7)).split()[0]
    url = "https://www.billboard.com/charts/hot-100/"+date
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())
    r = http.request('GET', url)
    soup = BeautifulSoup(r.data, "lxml")
    if position is not None:
        data_extractor(soup,position)
    else:
        for position in range(start_position, end_position+1):
            data_extractor(soup,position)
        
if __name__ == "__main__":
    scraper(date = '1988-1-1')