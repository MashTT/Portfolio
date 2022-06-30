import sys
from turtle import right
import pandas as pd
from PyQt6.QtWidgets import (QApplication, QVBoxLayout, QHBoxLayout, QGridLayout, 
                                                 QWidget, QCalendarWidget, QPushButton, QCheckBox, QSlider, QLineEdit, QLabel)
from PyQt6.QtCore import (Qt, pyqtSignal, QTimer, QTime)
from PyQt6.QtGui import (QIcon, QFont)
import scroller
import datetime as dt
import webbrowser
import re
 
 
class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()

 
 
class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Main Window')
        #self.setFixedSize(1300,900)
        
        #for newsfeed
        # self.timer = QTimer(self)
        # self.timer.timeout.connect(self.update)
        # self.timer.start(60000) # 1 minites => 60000
        
        # for clock
        self.timer2 = QTimer(self)
        self.timer2.timeout.connect(self.clock_time)
        self.timer2.start(1000)

        mainLayout = QGridLayout(self)
        newsfeedLayout = QVBoxLayout(self)
        otherLayout =  QVBoxLayout(self)


        # clndr
        vbox_cal = QVBoxLayout(self)
        cal = QCalendarWidget(self)
        cal.setFixedSize(500,400)
        vbox_cal.addWidget(cal)


        # clock
        self.clock = QLabel(self, objectName='label_clock')
        self.clock .setText(format(dt.datetime.now(),'%H:%M:%S'))

        
        #nikkei
        vbox_NIKKEI = QVBoxLayout(self)
        vbox_NIKKEI.setContentsMargins(0,0,0,0)
        self.df_NIKKEI = scroller.ScrapingNIKKEI()
        css_title = '''
            text-align: left;
            font-family: "メイリオ" ;
            padding: 0px;
            margin-top: 5px 0px 0px 0px;
            font-size: 18pt;
            '''
        
        css_label = '''
            text-align: left;
            font-family: "メイリオ" ;
            padding: 0px;
            margin: 0px;
            '''
            
        titlelabel_NIKKEI = ClickableLabel(self, objectName='title_NIKKEI')
        titlelabel_NIKKEI.setStyleSheet(css_title)
        titlelabel_NIKKEI.setText('日経経済新聞　適時開示ランキング')
        vbox_NIKKEI.addWidget(titlelabel_NIKKEI)
        vbox_NIKKEI.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        for r,code,com,ad,at,sec,c in zip(self.df_NIKKEI['rank'], self.df_NIKKEI['code'], self.df_NIKKEI['company'], self.df_NIKKEI['announcedDate'], self.df_NIKKEI['announcedTime'], self.df_NIKKEI['section'], self.df_NIKKEI['contents']):
            name = ad + ' ' + at + '     ' + code + ':' + com + c
            label = ClickableLabel(self, objectName='NIKKEI_label_' + r)
            label.setStyleSheet(css_label)
            label.setText(name)
            label.setMaximumWidth(800)
            label.clicked.connect(self.clicked)
            vbox_NIKKEI.addWidget(label)
        

        #news
        vbox_NewsAPI = QVBoxLayout(self)
        vbox_NewsAPI.setContentsMargins(0,0,0,0)
        
        self.df_NewsAPI = scroller.NewsAPI()
        
        titlelabel_NewsAPI = ClickableLabel(self, objectName='title_NewsAPI')
        titlelabel_NewsAPI.setStyleSheet(css_title)
        titlelabel_NewsAPI.setText('ビジネスニュース一覧')
        vbox_NewsAPI.addWidget(titlelabel_NewsAPI)
        vbox_NewsAPI.setAlignment(Qt.AlignmentFlag.AlignTop)
        i = 0

        for p, t, u in zip(self.df_NewsAPI['publishedAt'], self.df_NewsAPI['title'], self.df_NewsAPI['url']):
            i += 1
            d = dt.datetime.strptime(p,'%Y-%m-%dT%H:%M:%SZ')
            name = format(d, '%y/%m/%d %H:%M') + '     ' + t 

            label = ClickableLabel(self, objectName='NewsAPI_label_' + str(i))
            label.setStyleSheet(css_label)
            label.setText(name)
            label.setMaximumWidth(800)
            label.clicked.connect(self.clicked)
            vbox_NewsAPI.addWidget(label)
                

                        
        #add all layouts
        newsfeedLayout.addLayout(vbox_NIKKEI)
        newsfeedLayout.addLayout(vbox_NewsAPI)
        otherLayout.addLayout(vbox_cal)
        otherLayout.addWidget(self.clock)
        mainLayout.addLayout(newsfeedLayout,0,0)
        mainLayout.addLayout(otherLayout,0,1)
    
    
    def refresh_newsfeed(df, title):
        print('a')


    def clicked(self):
        label = self.sender()
        name = label.objectName()
        num = int(re.sub(r"\D", "", name)) - 1
        if num < 0:
            return

        elif 'NewsAPI' in name:
            d = self.df_NewsAPI.loc[[num], 'url']
            url = d.iloc[-1]
            webbrowser.open(url) 

        elif 'NIKKEI' in name:
            d = self.df_NIKKEI.loc[[num], 'code']
            url = 'https://www.buffett-code.com/company/' + str(d.iloc[-1]) + '/'
            webbrowser.open(url) 

    
    def refresh_news(self):
        print('pushed test1')
    
        
    def update(self):
        print("timer test")


    def clock_time(self):
        current_time = QTime.currentTime()
        label_time = current_time.toString('hh:mm:ss')

        if label_time[-2] == '5':
            css_clock = '''
                color: "#FF0000";
                font-size: 128px;
                font-family: Time;
                font-weight: bold;
                text-align: center;
            '''
        else:
            css_clock = '''
                color: "#008000";
                font-size: 128px;
                font-family: Time;
                font-weight: bold;
                text-align: center;
            '''
    
        self.clock.setText(label_time)
        self.clock.setStyleSheet(css_clock)

    
    
if __name__ == '__main__':
    app = QApplication(sys.argv) 
    main_window = MainWindow() 
    main_window.show() 
    app.exec() 