import kivy
kivy.require('1.9.1')

from kivy.graphics import Color,Rectangle
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from time import strftime
from kivy.properties import ObjectProperty

# from kivy.lang import Builder
# Builder.load_file('test.kv')

class MyWidgetClass(BoxLayout):
    pass

class TestApp(App):
    sw_seconds = 0
    sw_started = False

    # clock functions
    def update_time(self, clk):
        self.root.ids.time.text = strftime("[b]%H[/b]:%M.[size=40]%S[/size]")

    # def on_start(self):
    #     Clock.schedule_interval(self.update_time,1)

    #stopwatch functions
    def on_sw_start(self):
        Clock.schedule_interval(self.update_sw,0)

    def update_sw(self,nap):
        if self.sw_started:
            self.sw_seconds += nap
            minutes, seconds = divmod(self.sw_seconds,60)
            self.root.ids.stopwatch.text = ('%02d:%02d.[size=20]%02d[/size]' % (int(minutes), int(seconds), int(seconds*100%100)))
    # stopwatch control handlers
    def start_stop(self):
        self.root.ids.start_stop.text = ('Start'
            if self.sw_started else 'Stop')
        self.sw_started = not self.sw_started

    def reset(self):
        if self.sw_started:
            self.root.ids.start_stop.text = 'Start'
            self.sw_started = False
            self.sw_seconds = 0
            minutes, seconds = divmod(self.sw_seconds,60)
            self.root.ids.stopwatch.text = ('%02d:%02d.[size=20]%02d[/size]' % (int(minutes), int(seconds), int(seconds*100%100)))

        self.sw_seconds = 0

    def build(self):
        time_prop = ObjectProperty(None)
        self.on_sw_start()
        return MyWidgetClass()

if __name__ == '__main__':
    TestApp().run()
