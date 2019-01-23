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
        # self.rec_param = RecSetting().start()

        # Initialize variables
        self.fps = 30
        # self.cnt = 0
        self.pre_cnt = -1
        self.pre_timestamp = datetime.datetime.now()
        self.rec_flag = False

    def Update_Param(self):
        app = App.get_running_app()
        self.fps = app.Cam_fps
        print "FPS is set at " + str(self.fps)

    def Preview(self):
        # print('button pressed')
        # print self.fps
        Clock.unschedule(self.Preview_update)
        Clock.schedule_interval(self.Preview_update, 1.0 / self.fps)

    def Preview_update(self, dt):
        ret, frame, timestamp, count, Vwidth, Vheight = self.capture.read()

        if self.pre_cnt == -1:
            self.Vwidth = Vwidth
            self.Vheight = Vheight
            print '[PREVIEW] width: ' + str(self.Vwidth) + ', height: ' + str(self.Vheight)
        # print self.cnt
        if ret and count != self.pre_cnt:

            delta = timestamp - self.pre_timestamp
            delta_ms = int(delta.total_seconds() * 1000)
            est_fps = 1.0/delta_ms * 1000

            self.pre_cnt = count
            # self.frame = frame
            self.pre_timestamp = timestamp
            self.timestamp = timestamp
            # print 'preview ' + timestamp.strftime("%Y-%m-%d %H:%M:%S:%f")
            # print est_fps

            if self.rec_flag:
                # cv2.imshow("Frame", frame)
                self.video_out.write(frame)
                timestr = timestamp.strftime("%Y-%m-%d %H:%M:%S:%f") + '\n'
                self.txt_out.write(timestr)


            # Display preview iamge from webcam
            # convert it to texture
            # if self.rec_flag is False:
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
        print self.fps

        print '[RECORDING] width: ' + str(self.Vwidth) + ', height: ' + str(self.Vheight)

        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        self.video_out = cv2.VideoWriter(video_fname,fourcc,self.fps,(self.Vwidth,self.Vheight))
        self.txt_out = open(video_tname,'w')
        # self.out = out

        # self.fps = RecSetting.Read_FPS(self)
        # print self.fps
        # print 1.0 / self.fps
        self.rec_flag = True
        # Clock.schedule_interval(self.Rec_update, 1.0 / self.fps)

    def Rec_update(self, dt):
        pass
        # self.out.write(self.frame)
        # timestr = self.timestamp.strftime("%Y-%m-%d %H:%M:%S:%f") + '\n'
        # self.txt_out.write(timestr)


    def Stop_record(self):
        print('record stop')
        # Clock.unschedule(self.Rec_update)
        self.rec_flag = False
        self.video_out.release()
        self.txt_out.close()

    def Quit(self):
        Clock.unschedule(self.Preview_update)
        self.capture.release()
