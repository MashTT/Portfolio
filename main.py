import sys
import pandas as pd
from PyQt6.QtWidgets import (QApplication, QWidget, 
                             QPushButton, QCheckBox, 
                             QSlider, QLineEdit, 
                             QCalendarWidget, QProgressBar,
                             QVBoxLayout,QGridLayout,QLabel)
from PyQt6.QtCore import Qt , pyqtSignal
from PyQt6.QtGui import QIcon
import scroller
 
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
        self.setGeometry(400, 300, 600, 800) #self.move(400, 300), self.resize(400, 500)と一緒
        self.setWindowTitle('Main Window')
        
        layout = QGridLayout(self)
        #layout.setSpacing(20)

        # ボタン
        # btn = QPushButton('更新', self)
        # btn.move(100, 50)
        # btn.resize(btn.sizeHint()) # sizeHintでいいかんじの大きさにしてくれる
        # btn.clicked.connect(self.refresh_news)
        
        # # チェックボックス
        # cb = QCheckBox('Check Box', self)
        # cb.move(100, 100)
 
        # # テキストボックス
        # qle = QLineEdit(self)
        # qle.setGeometry(100, 200, 200, 20)

        # カレンダー
        cal = QCalendarWidget(self)
        #vbox.addWidget(cal,1,1)
        
        #nikkei
        vbox_NIKKEI = QVBoxLayout(self)
        vbox_NIKKEI.setContentsMargins(0,0,0,0)
        df = scroller.Scraping_NIKKEI()
        css = '''
            border: 1px solid white;
            text-align: left;
            padding: 0px;
            margin: 0px
            '''
            
        titlelabel_NIKKEI = ClickableLabel(self, objectName='label_NIKKEI')
        titlelabel_NIKKEI.setStyleSheet(css)
        titlelabel_NIKKEI.setText('日経経済新聞　適時開示ランキング')
        vbox_NIKKEI.addWidget(titlelabel_NIKKEI)
        
        for r,code,com,ad,at,sec,c in zip(df['rank'], df['code'], df['company'], df['announcedDate'], df['announcedTime'], df['section'], df['contents']):
            name = r + '. ' + ad + ' ' + at + '  ' + code + ':' + com + c
            label = ClickableLabel(self, objectName='label_NIKKEI' + r)
            
            label.setStyleSheet(css)
            label.setText(name)
            label.clicked.connect(self.clicked)
            vbox_NIKKEI.addWidget(label)
        
        
        #news
        vbox_NewsAPI = QVBoxLayout(self)
        vbox_NewsAPI.setContentsMargins(0,0,0,0)
        
        df = scroller.NewsAPI()
        css = '''
            border: 1px solid white;
            text-align: left;
            padding: 0px;
            margin: 0px
            '''
        
        titlelabel_NewsAPI = ClickableLabel(self, objectName='label_NewsAPI')
        titlelabel_NewsAPI.setStyleSheet(css)
        titlelabel_NewsAPI.setText('ビジネスニュース一覧')
        vbox_NewsAPI.addWidget(titlelabel_NewsAPI)
        
        i = 0

        for p, t, u in zip(df['publishedAt'], df['title'], df['url']):
            i += 1
            name = str(i) + '. ' + p + '   ' + t 
            label = ClickableLabel(self, objectName='label_NewsAPI' + str(i))
            label.setStyleSheet(css)
            label.setText(name)
            label.clicked.connect(self.clicked)
            vbox_NewsAPI.addWidget(label)
                
                        
        #add all layouts
        layout.addLayout(vbox_NIKKEI,0,0)
        layout.addLayout(vbox_NewsAPI,1,0)
        layout.addWidget(cal,0,1)



    def clicked(self):
        label = self.sender()
        name = label.objectName()
        print(f"{name} clicked")

    
    def refresh_news(self):
        print('pushed test1')

    
    
if __name__ == '__main__':
    app = QApplication(sys.argv) #PyQtで必ず呼び出す必要のあるオブジェクト
    main_window = MainWindow() #ウィンドウクラスのオブジェクト生成
    main_window.show() 
    app.exec() 