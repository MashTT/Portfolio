# -*- coding: utf-8 -*-
from asyncio import futures
import concurrent.futures
import datetime as dt
import os
from PyQt6.QtWidgets import (QApplication, QVBoxLayout,  QGridLayout, 
                                                 QWidget, QCalendarWidget,  QLabel)
from PyQt6.QtCore import (Qt,  QTimer, QTime, QEvent)
import re
import scroller
import settings
import sys
import webbrowser

 

class MainWindow(QWidget):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.initUI()


    def initUI(self):
        self.setWindowTitle('Main Window')
        self.setFixedSize(1300,850)
        self.mainLayout = QGridLayout(self)
        self.leftLayout = QVBoxLayout(self)
        self.rightLayout =  QVBoxLayout(self)
        # calendar 
        self.clndr  = QCalendarWidget(self)
        self.clndr.setFixedSize(500,350)
        self.vbox_clndr = QVBoxLayout(self)
        self.vbox_clndr.addWidget(self.clndr)        
        # clock
        self.clock = QLabel(format(dt.datetime.now(),'%H:%M:%S'), self, objectName='label_clock')
        # refresh
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_selecter)
        self.timer.start(settings.REFRESH_INTERVAL)
        #nikkei
        self.vbox_rank = QVBoxLayout(self)
        self.df_rank = scroller.scrape_nikkei()
        self.rank_title_label = QLabel('日経経済新聞　適時開示ランキング', self)
        self.rank_title_label.setStyleSheet(settings.CSS_TITLE)
        self.vbox_rank.addWidget(self.rank_title_label)
        if self.df_rank is not None:
            for i, (code, com, ad, at, c) in enumerate(zip(self.df_rank['code'], self.df_rank['company'], 
                                                            self.df_rank['announcedDate'], self.df_rank['announcedTime'], 
                                                            self.df_rank['contents'])):
                d = format(dt.datetime.strptime( ad + ' ' + at,'%y/%m/%d %H:%M' ), '%y/%m/%d %H:%M')
                name = d + '     ' + code + ':' + com + c
                self.nikkei_label = QLabel(name, self, objectName='NIKKEI_label_' + str(i))
                self.nikkei_label.setStyleSheet(settings.CSS_LABEL)
                self.nikkei_label.setMaximumWidth(750)
                self.nikkei_label.installEventFilter(self)
                self.vbox_rank.addWidget(self.nikkei_label)
        else:
            self.rank_title_label.setText('日経経済新聞　適時開示ランキング(ロードエラー)')

        #news
        self.vbox_news = QVBoxLayout(self)
        self.df_news = scroller.get_news_from_api()
        self.news_title_label = QLabel('ビジネスニュース一覧', self)
        self.news_title_label.setStyleSheet(settings.CSS_TITLE)
        self.vbox_news.addWidget(self.news_title_label)
        if self.df_news is not None:
            for i, (p, t) in enumerate(zip(self.df_news['publishedAt'], self.df_news['title'])):
                d = format(dt.datetime.strptime(p,'%Y-%m-%dT%H:%M:%SZ'), '%y/%m/%d %H:%M')
                self.news_label = QLabel(d + '     ' + t, self, objectName='NewsAPI_label_' + str(i))
                self.news_label.setStyleSheet(settings.CSS_LABEL)
                self.news_label.setMaximumWidth(750)
                self.news_label.installEventFilter(self)
                self.vbox_news.addWidget(self.news_label)
        else:
            self.news_title_label.setText('ビジネスニュース一覧(ロードエラー)')
        #add all layouts
        self.blank_label = QLabel(self)
        self.blank_label.setFixedSize(100,250)
        self.leftLayout.addLayout(self.vbox_rank)
        self.leftLayout.addLayout(self.vbox_news)
        self.rightLayout.addLayout(self.vbox_clndr)
        self.rightLayout.addWidget(self.blank_label)
        self.rightLayout.addWidget(self.clock)
        self.mainLayout.addLayout(self.leftLayout, 0, 0)
        self.mainLayout.addLayout(self.rightLayout, 0, 1)
        

    def eventFilter(self, object, event):
        if event.type() == QEvent.Type.MouseButtonPress:
            if event.button() == Qt.MouseButton.LeftButton:
                name = object.objectName()
                num = int(re.sub(r"\D", "", name)) 
                if num < 0:
                    return False
                elif 'NewsAPI' in name:
                    d = self.df_news.loc[[num], 'url']
                    url = d.iloc[-1]
                    webbrowser.open(url) 
                    return True
                elif 'NIKKEI' in name:
                    d = self.df_rank.loc[[num], 'code']
                    url = os.path.join('https://www.buffett-code.com/company/', str(d.iloc[-1]))
                    webbrowser.open(url)
                    return True
            return False
        return False
        

    def update_selecter(self):
        if  QTime.currentTime().toString('ss') == '00':
            with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
                executor.submit(self.update_time)
                executor.submit(self.update_news)
        else:
            self.update_time()
            

    def update_news(self):
        targetList = self.findChildren(QLabel)
        self.df_news = scroller.get_news_from_api()
        if self.df_news is None:
            return
        for i, (p, t) in enumerate(zip(self.df_news['publishedAt'], self.df_news['title'])):
            d = format(dt.datetime.strptime(p,'%Y-%m-%dT%H:%M:%SZ'), '%y/%m/%d %H:%M')
            for target in targetList:
                if target.objectName() == 'NewsAPI_label_' + str(i):
                    target.setText(d + '     ' + t )
                    break
                    
    
    def update_time(self):
        current_time = QTime.currentTime()
        label_time = current_time.toString('hh:mm:ss')
        self.clock.setText(label_time)
        if label_time[-2] == '5':
            self.clock.setStyleSheet(settings.CSS_CLOCK_FONT_BLACK)
        else:
            self.clock.setStyleSheet(settings.CSS_CLOCK_FONT_RED)
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    app.exec()