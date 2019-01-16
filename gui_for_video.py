# coding:utf-8
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.properties import ObjectProperty, ListProperty, StringProperty

import datetime
# from FramePSec import FramePSec
from CamVideoStream import CamVideoStream

import cv2

class KivyCamera(Image):
    def __init__(self, capture, fps, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.capture = capture
        self.fps = fps
        self.cnt = 0
        self.pre_timestamp = datetime.datetime.now()

    def Preview(self):
        print('button pressed')
        Clock.schedule_interval(self.update, 1.0 / self.fps)

    def update(self, dt):
        ret, frame, timestamp = self.capture.read()
        self.frame = frame
        self.timestamp = timestamp
        # print self.cnt
        if self.cnt>0:
            d_timestamp = timestamp - self.pre_timestamp
            self.pre_timestamp = timestamp
            # print d_timestamp*1000

        self.cnt += 1
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
        print('record start')
        cur_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        video_fname = './Recorded_Video/output_'+ cur_date + '.avi'
        video_tname = './Recorded_Video/output_ts_'+ cur_date + '.txt'
        print cur_date

        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        out = cv2.VideoWriter(video_fname,fourcc,30,(1920,1080))
        self.txt_out = open(video_tname,'w')
        self.out = out

        Clock.schedule_interval(self.rec_update, 1.0 / self.fps)

    def rec_update(self, dt):
        self.out.write(self.frame)
        timestr = self.timestamp.strftime("%Y-%m-%d %H:%M:%S:%f") + '\n'
        self.txt_out.write(timestr)

    def stop_record(self):
        print('record stop')
        Clock.unschedule(self.rec_update)
        self.out.release()
        self.txt_out.close()


class CamApp(App):
    def build(self):
        self.capture = CamVideoStream(src=0).start()
        self.my_camera = KivyCamera(capture=self.capture, fps=30)

        return self.my_camera

    def on_stop(self):
        #without this, app will not exit even if the window is closed
        self.capture.release()


if __name__ == '__main__':
    CamApp().run()
