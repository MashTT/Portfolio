import kivy
from kivy.app import App
from kivy.uix.label import Label
#import scroller
from kivy.lang import Builder
Builder.load_file('layout.kv')

class MainScreen(App):
    pass

    #def build(self):
        #str = scroller.NewsAPI
        #return Label( text = str )
        
if __name__ == '__main__':
    MainScreen().run()