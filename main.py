# -*- coding: utf-8 -*-

import datetime as dt
from PyQt6.QtWidgets import (QApplication, QVBoxLayout,  QGridLayout, 
                                                 QWidget, QCalendarWidget,  QLabel)
from PyQt6.QtCore import (Qt,  QTimer, QTime, QEvent)
import re
import scroller
import sys
import webbrowser

 
class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.initUI()


    def initUI(self):
        self.setWindowTitle('Main Window')
        self.setFixedSize(1300,850)
        mainLayout = QGridLayout(self)
        newsfeedLayout = QVBoxLayout(self)
        otherLayout =  QVBoxLayout(self)

        # clndr
        vbox_cal = QVBoxLayout(self)
        cal = QCalendarWidget(self)
        cal.setFixedSize(500,400)
        vbox_cal.addWidget(cal)
        
        # clock
        sTime = format(dt.datetime.now(),'%H:%M:%S')
        self.clock = QLabel(self, objectName='label_clock')
        self.clock .setText(sTime)

        # for clock refresh
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.clock_time)
        self.timer.start(1000)

        #for newsfeed refresh
        self.timer2 = QTimer(self)
        self.timer2.timeout.connect(self.update_news)
        self.timer2.start(60000) # 1 minites => 60000

        #nikkei
        vbox_NIKKEI = QVBoxLayout(self)
        self.df_NIKKEI = scroller.ScrapingNIKKEI()
        css_title = '''
            text-align: left;
            padding: 0px;
            margin-top: 5px 0px 0px 0px;
            font-size: 18pt;
            '''
        
        css_label = '''
            text-align: left;
            padding: 0px;
            margin: 0px;
            '''
            
        titlelabel_NIKKEI = QLabel(self)
        titlelabel_NIKKEI.setStyleSheet(css_title)
        titlelabel_NIKKEI.setText('日経経済新聞　適時開示ランキング')
        vbox_NIKKEI.addWidget(titlelabel_NIKKEI)
        
        for r,code,com,ad,at,sec,c in zip(self.df_NIKKEI['rank'], self.df_NIKKEI['code'], self.df_NIKKEI['company'], self.df_NIKKEI['announcedDate'], self.df_NIKKEI['announcedTime'], self.df_NIKKEI['section'], self.df_NIKKEI['contents']):
            d = dt.datetime.strptime(ad + ' ' + at,'%y/%m/%d %H:%M')
            name = format(d, '%y/%m/%d %H:%M')   + '     ' + code + ':' + com + c

            nikkei_label = QLabel(self)
            nikkei_label.setObjectName('NIKKEI_label_' + str(r))
            nikkei_label.setStyleSheet(css_label)
            nikkei_label.setText(name)
            nikkei_label.setMaximumWidth(800)
            nikkei_label.installEventFilter(self)
            vbox_NIKKEI.addWidget(nikkei_label)
        
        #news
        self.vbox_NewsAPI = QVBoxLayout(self)        
        self.df_NewsAPI = scroller.NewsAPI()
        titlelabel_NewsAPI = QLabel(self)
        titlelabel_NewsAPI.setStyleSheet(css_title)
        titlelabel_NewsAPI.setText('ビジネスニュース一覧')
        self.vbox_NewsAPI.addWidget(titlelabel_NewsAPI)
        i = 0

        for p, t, u in zip(self.df_NewsAPI['publishedAt'], self.df_NewsAPI['title'], self.df_NewsAPI['url']):           
            i += 1
            d = dt.datetime.strptime(p,'%Y-%m-%dT%H:%M:%SZ')
            name = format(d, '%y/%m/%d %H:%M') + '     ' + t 
            
            news_label = QLabel(self)
            news_label.setObjectName('NewsAPI_label_' + str(i))
            news_label.setStyleSheet(css_label)
            news_label.setText(name)
            news_label.setMaximumWidth(800)
            news_label.installEventFilter(self)
            self.vbox_NewsAPI.addWidget(news_label)
                        
        #add all layouts
        newsfeedLayout.addLayout(vbox_NIKKEI)
        newsfeedLayout.addLayout(self.vbox_NewsAPI)
        otherLayout.addLayout(vbox_cal)
        otherLayout.addWidget(self.clock, Qt.AlignmentFlag.AlignBottom)
        mainLayout.addLayout(newsfeedLayout,0,0)
        mainLayout.addLayout(otherLayout,0,1)
        

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
        targetList = self.findChildren(QLabel)
        self.df_NewsAPI = scroller.NewsAPI()
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
        current_time = QTime.currentTime()
        label_time = current_time.toString('hh:mm:ss')

        if label_time[-2] == '5':
            css_clock = '''                
                color: "#FF0000";
                font-size: 118px;
                font-weight: bold;
                text-align: right;
            '''
        else:
            css_clock = '''
                color: "#008000";
                font-size: 118px;
                font-weight: bold;
                text-align: right;
            '''
    
        self.clock.setText(label_time)
        self.clock.setStyleSheet(css_clock)

    
if __name__ == '__main__':
    app = QApplication(sys.argv) 
    main_window = MainWindow() 
    main_window.show() 
    app.exec() 