from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture

import datetime
from CamVideoStream import CamVideoStream
from RecSetting import RecSetting

import cv2

class CameraControl(Image):
    def __init__(self, **kwargs):
        super(CameraControl, self).__init__(**kwargs)
        self.capture = CamVideoStream(src=0).start()
        self.rec_param = RecSetting().start()
        self.fps = 30
        self.cnt = 0
        self.pre_timestamp = datetime.datetime.now()

    def Preview(self):
        print('button pressed')
        app = App.get_running_app()
        self.fps = app.Cam_fps
        print "FPS is set at " + str(self.fps)

        Clock.schedule_interval(self.Preview_update, 1.0 / self.fps)

    def Preview_update(self, dt):
        ret, frame, timestamp, width, height = self.capture.read()
        self.frame = frame
        self.timestamp = timestamp
        self.width = width
        self.height = height

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
        out = cv2.VideoWriter(video_fname,fourcc,self.fps,(self.width,self.height))
        self.txt_out = open(video_tname,'w')
        self.out = out

        self.fps = RecSetting.Read_FPS(self)
        print self.fps

        Clock.schedule_interval(self.Rec_update, 1.0 / self.fps)

    def Rec_update(self, dt):
        self.out.write(self.frame)
        timestr = self.timestamp.strftime("%Y-%m-%d %H:%M:%S:%f") + '\n'
        self.txt_out.write(timestr)

    def Stop_record(self):
        print('record stop')
        Clock.unschedule(self.rec_update)
        self.out.release()
        self.txt_out.close()

    def Quit(self):
        self.capture.release()
