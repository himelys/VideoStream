from kivy.uix.widget import Widget
from kivy.clock import Clock

class PostProcess(Widget):

    def __init__(self, **kwargs):
        super(PostProcess, self).__init__(**kwargs)
        # self.fps_set = 30

    # def start(self):
    #     # Clock.schedule_interval(self.Set_FPS, 0.1)
    #     return self
    #
    # def Set_FPS(self,value):
    #     self.fps_set = value
    #     print self.fps_set
    #     return self.fps_set
    #
    # def Read_FPS(self):
    #     return self.fps_set
