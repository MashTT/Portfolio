import requests
from bs4 import BeautifulSoup
import pandas as pd
#from newsapi import NewsApiClient


def Scraping_NIKKEI():

    url = "https://www.nikkei.com/markets/ranking/page/?bd=disclose" # 日本経済新聞 適宜開示ランキング

    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    table = soup.find('table') # rank_table
    thead = table.find('thead')  
    tbody = table.find('tbody') 

    for target in tbody.find_all('div'):
        target.decompose()

    for target in tbody.find_all('p'):
        target.decompose()

    for target in tbody.find_all('h6'):
        target.decompose()

    ths = thead.tr.find_all('th')
    trs = tbody.find_all('tr') 

    result = []
    temp = []  

    for th in ths:  # thead -> trからthタグを探す
        t = th.text
        temp.append(t.strip())  # thタグのテキストを保存

    result.append(temp) 

    for tr in trs:
        temp = []
        for td in tr.find_all('td'):  # trタグからtdタグを探す
            t = td.text
            temp.append(t.strip())  # tdタグのテキストを保存

        result.append(temp)

    #return result

    # 出力
    for temp in result:
        print(','.join(temp))  # カンマ（,）で列を結合して表示


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
        df = pd.DataFrame(data['articles'])
        print('totalResults:', data['totalResults'])

    print(df[[ 'publishedAt', 'title', 'url']])
    

NewsAPI()  #get news from NewsAPI
Scraping_NIKKEI() #get Viewing ranking of Timely disclosure 

