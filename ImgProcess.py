import cv2
import numpy as np

class ImgProcess:

    def __init__(self):
        pass

    def brightness_contrast(self,img,B,C):

        if B != 0:
            if B > 0:
                shadow = B
                highlight = 255
            else:
                shadow = 0
                highlight = 255 + B
            alpha_b = (highlight - shadow)/255
            gamma_b = shadow

            buf = cv2.addWeighted(img, alpha_b, img, 0, gamma_b)
        else:
            buf = img.copy()

        if C != 0:
            f = 131*(C + 127)/(127*(131-C))
            alpha_c = f
            gamma_c = 127*(1-f)

            buf = cv2.addWeighted(buf, alpha_c, buf, 0, gamma_c)

        return buf
