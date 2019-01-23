from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.properties import StringProperty

class RecStatus(Widget):
    str_frameSec = StringProperty()

    def __init__(self, **kwargs):
        super(RecStatus, self).__init__(**kwargs)
        self.str_frameSec = 'This is for test'

    def CurrentFPS(self, val):
        self.str_frameSec = str(val)
