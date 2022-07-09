# -*- coding: utf-8 -*-
import concurrent.futures
import datetime as dt
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
        self.newsfeedLayout = QVBoxLayout(self)
        self.otherLayout =  QVBoxLayout(self)

        # clndr
        self.cal = QCalendarWidget(self)
        self.cal.setFixedSize(500,400)
        self.vbox_cal = QVBoxLayout(self)
        self.vbox_cal.addWidget(self.cal)
        
        # clock
        sTime = format(dt.datetime.now(),'%H:%M:%S')
        self.clock = QLabel(self, objectName='label_clock')
        self.clock.setText(sTime)

        # for clock refresh
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.clock_time)
        self.timer.start(settings.CLOCK_REFRESH_INTERVAL)

        #for newsfeed refresh
        self.timer2 = QTimer(self)
        self.timer2.timeout.connect(self.update_news)
        self.timer2.start(settings.NEWS_REFRESH_INTERVAL)

        #nikkei
        self.vbox_NIKKEI = QVBoxLayout(self)
        self.df_NIKKEI = scroller.Scrape_NIKKEI()
        self.titlelabel_NIKKEI = QLabel(self)
        self.titlelabel_NIKKEI.setStyleSheet(settings.CSS_TITLE)
        self.titlelabel_NIKKEI.setText('日経経済新聞　適時開示ランキング')
        self.vbox_NIKKEI.addWidget(self.titlelabel_NIKKEI)
        
        if self.df_NIKKEI is not None:
            for r, code, com, ad, at, c in zip(self.df_NIKKEI['rank'], self.df_NIKKEI['code'], self.df_NIKKEI['company'], 
                                                            self.df_NIKKEI['announcedDate'], self.df_NIKKEI['announcedTime'], 
                                                            self.df_NIKKEI['contents']):
                d = dt.datetime.strptime( ad + ' ' + at,'%y/%m/%d %H:%M' )
                name = format(d, '%y/%m/%d %H:%M')   + '     ' + code + ':' + com + c

                self.nikkei_label = QLabel(self)
                self.nikkei_label.setAlignment(Qt.AlignmentFlag.AlignTop)
                self.nikkei_label.setObjectName('NIKKEI_label_' + str(r))
                self.nikkei_label.setStyleSheet(settings.CSS_LABEL)
                self.nikkei_label.setText(name)
                self.nikkei_label.setMaximumWidth(800)
                self.nikkei_label.installEventFilter(self)
                self.vbox_NIKKEI.addWidget(self.nikkei_label)
        else:
            self.titlelabel_NIKKEI.setText('日経経済新聞　適時開示ランキング(ロードエラー)')
        
        #news
        self.vbox_NewsAPI = QVBoxLayout(self)
        self.df_NewsAPI = scroller.NewsAPI()
        self.titlelabel_NewsAPI = QLabel(self)
        self.titlelabel_NewsAPI.setStyleSheet(settings.CSS_TITLE)
        self.titlelabel_NewsAPI.setText('ビジネスニュース一覧')
        self.vbox_NewsAPI.addWidget(self.titlelabel_NewsAPI)
        i = 0

        if self.df_NewsAPI is not None:
            for p, t, u in zip(self.df_NewsAPI['publishedAt'], self.df_NewsAPI['title'], self.df_NewsAPI['url']):
                i += 1
                d = dt.datetime.strptime(p,'%Y-%m-%dT%H:%M:%SZ')
                name = format(d, '%y/%m/%d %H:%M') + '     ' + t 
                
                self.news_label = QLabel(self)
                self.news_label.setObjectName('NewsAPI_label_' + str(i))
                self.news_label.setStyleSheet(settings.CSS_LABEL)
                self.news_label.setText(name)
                self.news_label.setMaximumWidth(800)
                self.news_label.installEventFilter(self)
                self.vbox_NewsAPI.addWidget(self.news_label)
        else:
            self.titlelabel_NewsAPI.setText('ビジネスニュース一覧(ロードエラー)')

        
        self.blank_label = QLabel(self)
        self.blank_label.setFixedSize(100,250)
        #add all layouts
        self.newsfeedLayout.addLayout(self.vbox_NIKKEI)
        self.newsfeedLayout.addLayout(self.vbox_NewsAPI)
        self.otherLayout.addLayout(self.vbox_cal)
        self.otherLayout.addWidget(self.blank_label)
        self.otherLayout.addWidget(self.clock)
        self.mainLayout.addLayout(self.newsfeedLayout, 0, 0)
        self.mainLayout.addLayout(self.otherLayout, 0, 1)
        

    def eventFilter(self, object, event):
        if event.type() == QEvent.Type.MouseButtonPress:
            if event.button() == Qt.MouseButton.LeftButton:
                name = object.objectName()
                num = int(re.sub(r"\D", "", name)) - 1
                if num < 0:
                    return True
                elif 'NewsAPI' in name:
                    d = self.df_NewsAPI.loc[[num], 'url']
                    url = d.iloc[-1]
                    webbrowser.open(url) 
                    return True
                elif 'NIKKEI' in name:
                    d = self.df_NIKKEI.loc[[num], 'code']
                    url = 'https://www.buffett-code.com/company/' + str(d.iloc[-1]) + '/'
                    webbrowser.open(url)
                    return True
            return False
        return False
        

    def update_news(self):
        with concurrent.futures.ProcessPoolExecutor() as executor:
            targetList = self.findChildren(QLabel)
            self.df_NewsAPI = scroller.NewsAPI()
            if self.df_NewsAPI is None:
                return
            i = 0

            for p, t in zip(self.df_NewsAPI['publishedAt'], self.df_NewsAPI['title']):
                i += 1 
                d = dt.datetime.strptime(p,'%Y-%m-%dT%H:%M:%SZ')
                newStr = format(d, '%y/%m/%d %H:%M') + '     ' + t 
                labelName = 'NewsAPI_label_' + str(i)
                for target in targetList:
                    if target.objectName() == labelName:
                        target.setText(newStr)
                        break
                        

    def clock_time(self):
        with concurrent.futures.ProcessPoolExecutor() as executor:
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