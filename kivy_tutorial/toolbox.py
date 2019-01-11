from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.clock import Clock
import time


class MyLayout(BoxLayout):
    your_time = StringProperty()
    def __init__(self,**kwargs):
        super(MyLayout,self).__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = 10
        Clock.schedule_interval(self.set_time, 0.1)

    def set_time(self,dt):
        self.your_time = time.strftime("%m/%d/%Y %H:%M")

class MyApp(App):
    def build(self):
        return MyLayout()


if __name__ == "__main__":
    MyApp().run()
