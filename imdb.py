# -*- coding: utf-8 -*-
"""
Created on Mon May 16 15:47:06 2022

@author: DennisLin
"""

import json
import requests
import math
from collections import Counter

API_KEY = 'c59989c6'
OMDB_URL = "http://www.omdbapi.com/?apikey=" + API_KEY

def get_data(url):
    data = json.loads(requests.get(url).text)
    if data['Response'] == 'True':
        return data
    else:
        return None
    
def search_ids_by_keyword(keywords):
    movie_ids = list()
    query = '+'.join(keywords.split())
    url = OMDB_URL + '&s=' + query
    data = get_data(url)
    if data:
        for item in data['Search']:
            movie_ids.append(item['imdbID'])
            total = int(data['totalResults'])
            num_pages = math.ceil(total/10)
            
        for i in range(2, num_pages + 1):
            url = OMDB_URL + '&s=' + query + '&page=' + str(i)
            data = get_data(url)
            if data:
                for item in data['Search']:
                    movie_ids.append(item['imdbID'])
    return movie_ids

def search_by_id(movie_id):
    url = OMDB_URL + "&i=" + movie_id
    data = get_data(url)
    return data if data else None

if __name__ == "__main__":
    keyword = "avengers"
    m_ids = search_ids_by_keyword(keyword)
    print("關鍵字 %s 共有 %d 部影片" % (keyword, len(m_ids)))
    print("取得資料影片...")
    movies = list()
    for m_id in m_ids:
        movies.append(search_by_id(m_id))
    print("影片資料範例")
    for m in movies[:3]:
        print(m)
    years = [m['Year'] for m in movies]
    year_dist = Counter(years)
    print("發行年份: ", year_dist)
    ratings = [float(m['imdbRating']) for m in movies if m['imdbRating'] != "N/A"]
    print('平均評分: ', sum(ratings)/len(ratings))