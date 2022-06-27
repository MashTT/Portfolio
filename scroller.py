import requests
from bs4 import BeautifulSoup

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

    return result

    # 出力
    for temp in result:
        print(','.join(temp))  # カンマ（,）で列を結合して表示


def Scraping_NIKKEI():
