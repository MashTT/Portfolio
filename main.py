from kivy.app import App
from kivy.clock import Clock
from kivy.properties import (
    ListProperty,
    NumericProperty,
    ObjectProperty,
    ReferenceListProperty,
)
from kivy.uix.widget import Widget
from kivy.vector import Vector


from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.treeview import TreeView, TreeViewLabel, TreeViewNode
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.resources import resource_add_path

    
    

class Player(Widget):
    """プレイヤー"""

    pass

 
class Shot(Widget):
    """プレイヤーの弾"""

    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(10)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        """弾の移動処理"""

        self.pos = Vector(*self.velocity) + self.pos


class ShootingGame(Widget):
    """ルートウィジェット。シューティングゲーム全体の管理"""

    player = ObjectProperty(None)
    shots = ListProperty()

    def on_touch_move(self, touch):
        """タッチしたまま移動でプレイヤー移動"""

        if 0 < touch.x < self.width:
            self.player.center_x = touch.x

    def on_touch_down(self, touch):
        """画面タッチで弾発射"""

        shot = Shot(pos=self.player.center)
        self.shots.append(shot)
        self.add_widget(shot)

    def update(self, dt):
        """1/60秒毎に呼ばれる、ゲーム更新処理

        各ショットの移動処理や、敵キャラの移動、それぞれの衝突判定を行う
        """

        for ball in self.shots:
            ball.move()
            if (ball.y < self.y) or (ball.top > self.top):
                self.remove_widget(ball)
                self.shots.remove(ball)


class ShootingApp(App):

    def build(self):
        game = ShootingGame()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game

ShootingApp().run()
