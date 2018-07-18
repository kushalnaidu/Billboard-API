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
import os
class BillboardData:
    def _validate_date(self,date):
        date_in_string = date.split('-')
        if len(date_in_string[1]) < 2:
            date_in_string[1] = '0'+date_in_string[1]
        if len(date_in_string[2]) < 2:
            date_in_string[2] = '0'+date_in_string[2]
            date = '-'.join(date_in_string)
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
            
    def __init__(self,date = None,position = None, start_position = 1, end_position = 100, csv = False, name_of_csv = "Billboard.csv", reset_csv = True):
        self.date = date
        self.position = position
        self.start_position = start_position
        self.end_position = end_position
        self.csv = csv
        self.reset_csv = reset_csv
        self.name_of_csv = name_of_csv
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
        recorded_data = []
        if self.position is not None:
            recorded_data.append(self._data_extractor(soup,self.position))
        else:
            for position in range(self.start_position, self.end_position+1):
                try:
                    recorded_data.append(self._data_extractor(soup,position))
                except:
                    continue        #Older charts do not have all 100 songs listed.
        print("Rank {:^40} - {:^40}".format("Song Name","Artist"));
        count = 1
        for value in recorded_data:
            print("{:03}. {:^40} - {:^40}".format(count,value[0],value[1]))
            count+=1
        if self.csv is True:
            if self.reset_csv == False:
                flag = 'a'
            else:
                flag = 'w'
            with open(self.name_of_csv, flag, newline='') as f:
                writer = csv.writer(f)
                writer.writerows(recorded_data)

class ArchivedYearData:
    def __init__(self,year, position = None, start_position = 1, end_position = 100,csv = False):
        self.year = year
        self.position = position
        self.start_position = start_position
        self.end_position = end_position
        self.csv = csv
        name_of_file = "Billboard_"+str(year)+".csv"
        if(os.path.exists(name_of_file)):
            os.remove(name_of_file)
        if(year == datetime.now().year):
            date = datetime(year,1,1)
            while(date.month < datetime.now().month):
                print("date: {}".format(str(date).split()[0]))
                BillboardData(date = str(date).split()[0],position = position,start_position = 1, end_position = 100,csv = self.csv,name_of_csv = name_of_file, reset_csv = False)
                date += timedelta(days = 7)
            while(date <= datetime.today()-timedelta(days=7)):
                BillboardData(date = str(date).split()[0],position = position,start_position = 1, end_position = 100,csv = self.csv,name_of_csv = name_of_file, reset_csv = False)
                date += timedelta(days = 7)
        else:
            input_year = year
            date = datetime(year,1,1)
            while(year == date.year):
                print("date: {}".format(str(date).split()[0]))
                BillboardData(date = str(date).split()[0],position = position,start_position = 1, end_position = 100,csv = self.csv,name_of_csv = name_of_file, reset_csv = False)
                date += timedelta(days = 7)
if __name__ == "__main__":
    x = ArchivedYearData(year = 2018,csv = True)
    