import sys
import pandas as pd
from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, QCheckBox, 
                             QSlider, QLineEdit, QCalendarWidget, QProgressBar,
                             QVBoxLayout, QHBoxLayout, QGridLayout, QLabel)
from PyQt6.QtCore import (Qt , pyqtSignal, QTimer)
from PyQt6.QtGui import (QIcon, QFont)
import scroller
import datetime as dt
 
class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def mousePressEvent(self, event):
        #if event.button() == Qt.LeftButton:
        self.clicked.emit()

 
 
class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.initUI()

    def initUI(self):
        #self.setGeometry(400, 300, 600, 800) 
        self.setWindowTitle('Main Window')
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(300000) # 5 minites => 300000
        
        mainLayout = QGridLayout(self)
        newsfeedLayout = QVBoxLayout(self)
        otherLayout =  QVBoxLayout(self)
        
        # clndr
        cal = QCalendarWidget(self)
        
        # clock
        clock = QLabel(self, objectName='label_clock')
        clock.setText(str(dt.datetime.now()))
        clock.move(50,20)
        
        
        #nikkei
        vbox_NIKKEI = QVBoxLayout(self)
        vbox_NIKKEI.setContentsMargins(0,0,0,0)
        df = scroller.Scraping_NIKKEI()
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
            
        titlelabel_NIKKEI = ClickableLabel(self, objectName='label_NIKKEI')
        titlelabel_NIKKEI.setStyleSheet(css_title)
        titlelabel_NIKKEI.setText('日経経済新聞　適時開示ランキング')
        titlelabel_NIKKEI.setFont(QFont('Times', 14))
        vbox_NIKKEI.addWidget(titlelabel_NIKKEI)
        vbox_NIKKEI.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        for r,code,com,ad,at,sec,c in zip(df['rank'], df['code'], df['company'], df['announcedDate'], df['announcedTime'], df['section'], df['contents']):
            name = ad + ' ' + at + '     ' + code + ':' + com + c
            label = ClickableLabel(self, objectName='label_NIKKEI' + r)
            label.setStyleSheet(css_label)
            label.setText(name)
            label.setMaximumWidth(800)
            label.clicked.connect(self.clicked)
            vbox_NIKKEI.addWidget(label)
        
        #news
        vbox_NewsAPI = QVBoxLayout(self)
        vbox_NewsAPI.setContentsMargins(0,0,0,0)
        
        df = scroller.NewsAPI()
        
        titlelabel_NewsAPI = ClickableLabel(self, objectName='label_NewsAPI')
        titlelabel_NewsAPI.setStyleSheet(css_title)
        titlelabel_NewsAPI.setText('ビジネスニュース一覧')
        vbox_NewsAPI.addWidget(titlelabel_NewsAPI)
        vbox_NewsAPI.setAlignment(Qt.AlignmentFlag.AlignTop)
        i = 0

        for p, t, u in zip(df['publishedAt'], df['title'], df['url']):
            i += 1
            d = dt.datetime.strptime(p,'%Y-%m-%dT%H:%M:%SZ')
            name = format(d, '%y/%m/%d %H:%M') + '     ' + t 
            label = ClickableLabel(self, objectName='label_NewsAPI' + str(i))
            label.setStyleSheet(css_label)
            label.setText(name)
            label.setMaximumWidth(800)
            label.clicked.connect(self.clicked)
            vbox_NewsAPI.addWidget(label)
                

                        
        #add all layouts
        newsfeedLayout.addLayout(vbox_NIKKEI)
        newsfeedLayout.addLayout(vbox_NewsAPI)
        otherLayout.addWidget(cal)
        otherLayout.addWidget(clock)
        mainLayout.addLayout(newsfeedLayout,0,0)
        mainLayout.addLayout(otherLayout,0,1)
    
    
    def refresh_newsfeed(df, title):
        print('a')


    def clicked(self):
        label = self.sender()
        name = label.objectName()
        print(f"{name} clicked")

    
    def refresh_news(self):
        print('pushed test1')
    
        
    def update(self):
        print("timer test")

    
    
if __name__ == '__main__':
    app = QApplication(sys.argv) 
    main_window = MainWindow() 
    main_window.show() 
    app.exec() 