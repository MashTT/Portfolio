import requests
from bs4 import BeautifulSoup
import pandas as pd

def Scraping_NIKKEI():

    url = "https://www.nikkei.com/markets/ranking/page/?bd=disclose" # 日本経済新聞 適宜開示ランキング
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    table = soup.find('table') # rank_table
    tbody = table.find('tbody') 
    delete_tag = ['div', 'p', 'h6']
    
    #remove 'unnecessary' tag
    for tag in delete_tag:
        for target in tbody.find_all(tag):
            target.decompose()
            

    trs = tbody.find_all('tr') 

    result = []
    tempHead = [ 'rank', 'code', 'company', 'announcedDate', 'announcedTime', 'section', 'contents' ]
    tempBody = []

    # tbody -> tr 
    for tr in trs:
        tempBody = []

        for td in tr.find_all('td'): 
            t = td.text
            tempBody.append(t.strip())
        
        tempBody.pop(0)
        result.append(tempBody)

    df_NIKKEI = pd.DataFrame( result, columns = tempHead )    

    #print(df_NIKKEI[[ 'rank', 'code', 'company', 'announcedDate', 'announcedTime', 'section', 'contents' ]])
    return df_NIKKEI




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
    else:
        df_NewsAPI = pd.DataFrame({ 'publishedAt' : '',
                                    'title' : '取得できませんでした。',
                                    'url' : ''
                                    })

    
    # print(df_NewsAPI[[ 'publishedAt', 'title', 'url' ]])
    return df_NewsAPI
    
    
    
#NewsAPI()  #get news from NewsAPI
Scraping_NIKKEI() #get Viewing ranking of Timely disclosure 

