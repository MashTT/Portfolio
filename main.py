import sys
from PyQt6.QtWidgets import (QApplication, QWidget, 
                             QPushButton, QCheckBox, 
                             QSlider, QLineEdit, 
                             QCalendarWidget, QProgressBar)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
 
class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setGeometry(400, 300, 600, 800) #self.move(400, 300), self.resize(400, 500)と一緒
        self.setWindowTitle('Main Window')

        # ボタン
        btn = QPushButton('更新', self)
        btn.move(100, 50)
        btn.resize(btn.sizeHint()) # sizeHintでいいかんじの大きさにしてくれる
        btn.clicked.connect(self.refresh_news)
        
        # チェックボックス
        cb = QCheckBox('Check Box', self)
        cb.move(100, 100)
 
        # テキストボックス
        qle = QLineEdit(self)
        qle.setGeometry(100, 200, 200, 20)

        # プログレスバー
        pbar = QProgressBar(self)
        pbar.setGeometry(100, 250, 200, 25)

        # カレンダー
        cal = QCalendarWidget(self)
        cal.move(100, 300)
    
    
    def refresh_news(self):
        print('pushed test1')

    
    
if __name__ == '__main__':
    app = QApplication(sys.argv) #PyQtで必ず呼び出す必要のあるオブジェクト
    main_window = MainWindow() #ウィンドウクラスのオブジェクト生成
    main_window.show() #ウィンドウの表示
    app.exec() #プログラム終了