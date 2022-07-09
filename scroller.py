# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import pandas as pd
import requests
import settings

def Scrape_NIKKEI():
    response = requests.get(settings.NIKKEI_URL)
    if response.ok:
        soup = BeautifulSoup(response.content, "html.parser")
        response.close()
        table = soup.find('table') # rank_table
        tbody = table.find('tbody')
        delete_tag = ['div', 'p', 'h6']
        #remove 'unnecessary' tag
        for tag in delete_tag:
            for target in tbody.find_all(tag):
                target.decompose()

        result = []
        tempHead = ['rank', 'code', 'company', 'announcedDate', 'announcedTime', 'section', 'contents']

        for tr in tbody.find_all('tr'):
            tempBody = []

            for td in tr.find_all('td'):
                t = td.text
                tempBody.append(t.strip())
            
            tempBody.pop(0) #remove firstline
            result.append(tempBody)

        df_NIKKEI = pd.DataFrame(result, columns = tempHead)
    else:
        df_NIKKEI = None
    
    return df_NIKKEI

def NewsAPI():    
    response = requests.get(settings.NEWS_API_URL, headers=settings.NEWS_API_HEADERS, params=settings.NEWS_API_PARAMS)

    if response.ok:
        data = response.json()
        df_NewsAPI = pd.DataFrame(data['articles'])
    else:
        df_NewsAPI = None

    return df_NewsAPI