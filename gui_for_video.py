# coding:utf-8
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture

from FramePSec import FramePSec
from CamVideoStream import CamVideoStream

import cv2


class KivyCamera(Image):
    def __init__(self, capture, fps, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.capture = capture
        self.fps = fps
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        out = cv2.VideoWriter('output2.avi',fourcc,30,(1920,1080))
        self.out = out
        #Clock.schedule_interval(self.update, 1.0 / fps)

    def Preview(self):
        Clock.schedule_interval(self.update, 1.0 / self.fps)

    def update(self, dt):
        ret, frame, cnt = self.capture.read()
        self.frame = frame
        if ret:
            # convert it to texture
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tostring()
            image_texture = Texture.create(
                size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            # display image from the texture
            self.texture = image_texture

    def Record(self):
        Clock.schedule_interval(self.rec_update, 1.0 / self.fps)

    def rec_update(self, dt):
            self.out.write(self.frame)
    def stop_record(self):
            self.out.release()

class start_record(Widget):
    pass


class CamApp(App):
    def build(self):
        self.capture = CamVideoStream(src=0).start()#cv2.VideoCapture(0)
        self.my_camera = KivyCamera(capture=self.capture, fps=30)
        # vs = CamVideoStream(src=0).start()
        # fps = FramePSec().start()
        return self.my_camera

    def on_stop(self):
        #without this, app will not exit even if the window is closed
        self.capture.release()


if __name__ == '__main__':
    CamApp().run()
