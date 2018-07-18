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
import csv

class BillboardData:
    def _validate_date(self,date):
        date = date.split('-')
        if len(date[1]) < 2:
            date[1] = '0'+date[1]
        if len(date[2]) < 2:
            date[2] = '0'+date[2]
            date = '-'.join(date)
        first_date = datetime(1958,8,4)
        if datetime.strptime(date, '%Y-%m-%d') < first_date:
            date = str(first_date).split()[0]
        if datetime.strptime(date, '%Y-%m-%d') > datetime.today()-timedelta(days = 7):
            date = str(datetime.today()-timedelta(days=7)).split()[0]
        try:
            datetime.strptime(date, '%Y-%m-%d')
            return date;
        except ValueError:
            raise ValueError("Incorrect data format, should be YYYY-MM-DD")
            
    def __init__(self,date = None,position = None, start_position = 1, end_position = 100, csv = False):
        self.date = date
        self.position = position
        self.start_position = start_position
        self.end_position = end_position
        self.csv = csv
        if date is None:
            self.date = str(datetime.today()-timedelta(days=7)).split()[0]
        else:
            self.date = self._validate_date(self.date)
        
        self.scrape()
        
        
        
    def _data_extractor(self,soup, position):
        if position is not 1 :
            attribute_class = 'chart-details'
            article = soup.find('div', attrs = {'class':attribute_class})
            song = article.find('div', attrs = {'data-rank':str(position)})
            song_name = song.attrs['data-title']
            artist_name = song.attrs['data-artist']
           
        else:
            attribute_class = 'chart-number-one__info'
            article = soup.find('div', attrs = {'class':attribute_class})
            song = article.find('div', attrs = {'class':'chart-number-one__title'})
            artist = article.find('div', attrs = {'class':'chart-number-one__artist'})
            song_name = song.text.strip()
            artist_name = artist.text.strip()
        return [song_name,artist_name]
            
    def scrape(self):
        
        
        
        url = "https://www.billboard.com/charts/hot-100/"+self.date
        http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())
        r = http.request('GET', url)
        soup = BeautifulSoup(r.data, "lxml")
        data = []
        if self.position is not None:
            self._data_extractor(soup,self.position)
        else:
            for position in range(self.start_position, self.end_position+1):
                try:
                    data.append(self._data_extractor(soup,position))
                except:
                    continue        #Older charts do not have all 100 songs listed.
        print("{:^40} - {:^40}".format("Song Name","Artist"));
        for value in data:
            print("{:^40} - {:^40}".format(value[0],value[1]))
        if self.csv is True:
            pass
        
if __name__ == "__main__":
    x = BillboardData(date = '2018-1-1',csv = True)
    