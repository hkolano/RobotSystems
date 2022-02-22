#!/usr/bin/python3
# coding=utf8
import sys
sys.path.append('/home/pi/ArmPi/')
import cv2
import time
import Camera
import threading
from LABConfig import *
from ArmIK.Transform import *
from ArmIK.ArmMoveIK import *
import HiwonderSDK.Board as Board
from CameraCalibration.CalibrationConfig import *

if sys.version_info.major == 2:
    print('Please run this program with python3!')
    sys.exit(0)

class ColorTracker():

    def __init__(self):
        self.img_size = (640, 480)
        pass

    def prepare_image(self, img):
        self.og_img = img 
        self.img_copy = img.copy()
        self.img_h, self.img_w = img.shape[:2]
        
        frame_resize = cv2.resize(self.img_copy, self.img_size, interpolation=cv2.INTER_NEAREST)
        return frame_resize


if __name__ == '__main__':
    p = ColorTracker()
    my_camera = Camera.Camera() 
    my_camera.camera_open()
    while True:
        img = my_camera.frame
        if img is not None:
            frame = p.prepare_image(img)
            cv2.imshow('Frame', frame)
            key = cv2.waitKey(1)
            if key == 27:
                break 
    my_camera.camera_close()
    cv2.destroyAllWindows()