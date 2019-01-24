#kivy.require("1.8.0")
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.properties import ObjectProperty, ListProperty, StringProperty, NumericProperty

import datetime

from CameraControl import CameraControl
from RecSetting import RecSetting


class PostProcess(Widget):
    pass
class MainScreen(Screen):
    pass
class SettingScreen(Screen):
    pass
class PostProcessScreen(Screen):
    pass
class ScreenManagement(ScreenManager):
    pass

presentation = Builder.load_file("main_gui.kv")

class MainApp(App):
    def build(self):
        return presentation

MainApp().run()


# ===================================================================
# Unused code

# class DebugPanel(Widget):
#     fps_measured = StringProperty(None)
#     def __init__(self, **kwargs):
#         super(DebugPanel, self).__init__(**kwargs)
#         Clock.schedule_once(self.update_fps, .03)
#
#     def update_fps(self,dt):
#         self.fps_measured = str(int(Clock.get_fps()))
#         Clock.schedule_once(self.update_fps, .03)
