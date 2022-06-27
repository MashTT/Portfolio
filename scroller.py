import requests
from bs4 import BeautifulSoup
import pandas as pd

def Scraping_NIKKEI():

    url = "https://www.nikkei.com/markets/ranking/page/?bd=disclose" # 日本経済新聞 適宜開示ランキング
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    table = soup.find('table') # rank_table
    tbody = table.find('tbody') 

    #remove 'unnecessary' tag
    for target in tbody.find_all('div'):
        target.decompose()

    for target in tbody.find_all('p'):
        target.decompose()

    for target in tbody.find_all('h6'):
        target.decompose()

    trs = tbody.find_all('tr') 

    result = []
    tempHead = [ 'rank', 'code', 'company', 'announcedDate', 'announcedTime', 'section', 'contents' ]
    tempBody = []

    # tbody -> trからtrタグを探す
    for tr in trs:
        tempBody = []

        for td in tr.find_all('td'): 
            t = td.text
            tempBody.append(t.strip())
        
        tempBody.pop(0)
        result.append(tempBody)

    df_NIKKEI = pd.DataFrame( result, columns  = tempHead )    
    #print(df_NIKKEI[[ 'rank', 'code', 'company', 'announcedDate', 'announcedTime', 'section', 'contents' ]])


def NewsAPI():
    #key = '0a2e80170ef3498a92c1bc275a6820b5'
    headers = {'X-Api-Key': '0a2e80170ef3498a92c1bc275a6820b5'}
    url = 'https://newsapi.org/v2/top-headlines' #NewsAPI top-headlines
    params = {
        'category': 'business',
        'country': 'jp'
    }

    response = requests.get(url, headers=headers, params=params)

    if response.ok:
        data = response.json()
        df_NewsAPI = pd.DataFrame(data['articles'])

    #print(df_NewsAPI[[ 'publishedAt', 'title', 'url']])




NewsAPI()  #get news from NewsAPI
Scraping_NIKKEI() #get Viewing ranking of Timely disclosure 

