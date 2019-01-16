from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.button import Button

import cv2
from FramePSec import FramePSec
from CamVideoStream import CamVideoStream


class VideoOut(Image):
    def __init__(self, capture, fps, **kwargs):
        super(VideoOut, self).__init__(**kwargs)
        self.capture = capture
        self.fps = fps
        # fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        # out = cv2.VideoWriter('output2.avi',fourcc,30,(1920,1080))
        # self.out = out

        Clock.schedule_interval(self.update, 1.0 / fps)

    # def Preview(self):
    #     Clock.schedule_interval(self.update, 1.0 / self.fps)

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
    # def Record(self):
    #     Clock.schedule_interval(self.rec_update, 1.0 / self.fps)
    #
    # def rec_update(self, dt):
    #         self.out.write(self.frame)
    # def stop_record(self):
    #         self.out.release()

# class KistScopeCreator(Widget):
#     # vs = CamVideoStream(src=0).start()
#     # fps = FramePSec().start()
#     def scope_start(self):
#         self.capture = CamVideoStream(src=0).start()#cv2.VideoCapture(0)
#         self.my_camera = VideoOut(capture=self.capture, fps=30)
#         return self.my_camera
#
#     def on_stop(self):
#         #without this, app will not exit even if the window is closed
#         self.capture.release()
class buttontest(object):
    def callback(self):
        print('The button is being pressed')

        self.capture = CamVideoStream(src=0).start()#cv2.VideoCapture(0)
        self.my_camera = VideoOut(capture=self.capture, fps=30)
        return my_camera

class CamApp(App):

    def build(self):
        self.img1 = Image()
        self.btn1 = Button(text='Preview', size_hint=(0.9,0.1),pos=(5,5),font_size=14)
        layout = BoxLayout()
        layout.add_widget(self.img1)
        layout.add_widget(self.btn1)
        self.btn1.bind(on_press=buttontest.callback)

        return layout

        # self.capture = CamVideoStream(src=0).start()#cv2.VideoCapture(0)
        # self.my_camera = VideoOut(capture=self.capture, fps=30)
        # return self.my_camera

    # def on_stop(self):
    #     #without this, app will not exit even if the window is closed
    #     self.capture.release()

        # return layout

    # def update(self, dt):
    #     # display image from cam in opencv window
    #     ret, frame = self.capture.read()
    #     # cv2.imshow("CV2 Image", frame)
    #     # convert it to texture
    #     buf1 = cv2.flip(frame, 0)
    #     buf = buf1.tostring()
    #     texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
    #     texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
    #     # display image from the texture
    #     self.img1.texture = texture1

if __name__ == '__main__':
    CamApp().run()
    # cv2.destroyAllWindows()
