# -*- coding: utf-8 -*-

#Timer
REFRESH_INTERVAL = 1000

#Scrape Nikkei
NIKKEI_URL = "https://www.nikkei.com/markets/ranking/page/?bd=disclose" # 日本経済新聞 適宜開示ランキング

#News API 
#key = '0a2e80170ef3498a92c1bc275a6820b5'
NEWS_API_URL = 'https://newsapi.org/v2/top-headlines' #NewsAPI top-headlines
NEWS_API_HEADERS = {'X-Api-Key': '0a2e80170ef3498a92c1bc275a6820b5'}
NEWS_API_PARAMS = {'category': 'business', 'country': 'jp'}

#label css
CSS_TITLE = '''
        text-align: left;
        padding: 0px;
        margin-top: 5px 0px 0px 0px;
        font-size: 18pt;
        '''
CSS_LABEL = '''
        text-align: left;
        padding: 0px;
        margin: 0px;
        '''
CSS_CLOCK_FONT_BLACK = '''
        color: "#FF0000";
        font-size: 128px;
        font-weight: bold;
        '''
CSS_CLOCK_FONT_RED = '''
        color: "#008000";
        font-size: 128px;
        font-weight: bold;
        '''