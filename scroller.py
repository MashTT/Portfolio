# -*- coding: utf-8 -*-

from urllib import response
from bs4 import BeautifulSoup
import pandas as pd
import requests


def ScrapingNIKKEI():

    url = "https://www.nikkei.com/markets/ranking/page/?bd=disclose" # 日本経済新聞 適宜開示ランキング
    response = requests.get(url)
    if response.ok:
        soup = BeautifulSoup(response.content, "html.parser")
        table = soup.find('table') # rank_table
        tbody = table.find('tbody')
        delete_tag = ['div', 'p', 'h6']
        #remove 'unnecessary' tag        
        for tag in delete_tag:
            for target in tbody.find_all(tag):
                target.decompose()       

        result = []
        tempHead = [ 'rank', 'code', 'company', 'announcedDate', 'announcedTime', 'section', 'contents' ]

        for tr in tbody.find_all('tr') :
            tempBody = []

            for td in tr.find_all('td'): 
                t = td.text
                tempBody.append(t.strip())
            
            tempBody.pop(0) #remove firstline
            result.append(tempBody)

        df_NIKKEI = pd.DataFrame( result, columns = tempHead )    
    else:
        df_NIKKEI = pd.DataFrame( {'contents' : '取得出来ませんでした。' }, columns = tempHead )    
    
    return df_NIKKEI


def NewsAPI():
    #key = '0a2e80170ef3498a92c1bc275a6820b5'
    headers = {'X-Api-Key': '0a2e80170ef3498a92c1bc275a6820b5'}
    url = 'https://newsapi.org/v2/top-headlines' #NewsAPI top-headlines
    params = {'category': 'business', 'country': 'jp'}
    response = requests.get(url, headers=headers, params=params)

    if response.ok:
        data = response.json()
        df_NewsAPI = pd.DataFrame(data['articles'])
    else:
        df_NewsAPI = pd.DataFrame({ 'publishedAt' : '', 'title' : '取得できませんでした。', 'url' : '' })

    return df_NewsAPI