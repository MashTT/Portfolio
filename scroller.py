# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import pandas as pd
import requests
import settings


def scrape_nikkei():
    response = requests.get(settings.NIKKEI_URL, timeout=3.5)
    if response.ok:
        soup = BeautifulSoup(response.content, "html.parser")
        response.close()
        table = soup.find('table')
        tbody = table.find('tbody')
        delete_tag = ['div', 'p', 'h6']
        #remove 'unnecessary' tag
        for tag in delete_tag:
            for target in tbody.find_all(tag):
                target.decompose()
        tempHead = ['rank', 'code', 'company', 'announcedDate', 'announcedTime', 'section', 'contents']
        result = []
        for tr in tbody.find_all('tr'):
            tempBody = [td.text.strip() for td in tr.find_all('td')]
            tempBody.pop(0) #remove firstline
            result.append(tempBody)
        df_rank = pd.DataFrame(result, columns = tempHead)
    else:
        df_rank = None
    return df_rank


def get_news_from_api():    
    response = requests.get(settings.NEWS_API_URL, headers=settings.NEWS_API_HEADERS, params=settings.NEWS_API_PARAMS, timeout=3.5)
    if response.ok:
        data = response.json()
        df_news = pd.DataFrame(data['articles'])
    else:
        df_news = None
    return df_news