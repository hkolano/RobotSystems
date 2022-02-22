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

    def detect_cube_center(self, img):
        self.prepare_image(img)
        return self.detect_color_contours('red')

    def prepare_image(self, img):
        self.og_img = img 
        self.img_copy = img.copy()
        self.img_h, self.img_w = img.shape[:2]
        
        # Resize the image
        frame_resize = cv2.resize(self.img_copy, self.img_size, interpolation=cv2.INTER_NEAREST)
        # Blur the image
        frame_gb = cv2.GaussianBlur(frame_resize, (11, 11), 11)
        # Convert to LAB color space
        frame_lab = cv2.cvtColor(frame_gb, cv2.COLOR_BGR2LAB)
        self.prepped_img = frame_lab

    def detect_color_contours(self, detect_color):
        frame_mask = cv2.inRange(self.prepped_img, color_range[detect_color][0], color_range[detect_color][1])
        # Erosion then dilation of mask
        opened = cv2.morphologyEx(frame_mask, cv2.MORPH_OPEN, np.ones((6, 6), np.uint8)) 
        # dilation then erosion of mask
        closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, np.ones((6, 6), np.uint8)) 
        # look at the mask for contours, select the biggest
        contours = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2] 
        areaMaxContour, area_max = self.getAreaMaxContour(contours)  # 找出最大轮廓 find the largest contour
        print("max area is: {}".format(area_max))
        return frame_mask

    def getAreaMaxContour(self, contours):
        contour_area_temp = 0
        contour_area_max = 0
        area_max_contour = None

        for c in contours:  # iterate over all contours
            contour_area_temp = math.fabs(cv2.contourArea(c))  # calculate the contour area
            if contour_area_temp > contour_area_max:
                contour_area_max = contour_area_temp
                if contour_area_temp > 300:  # The contour with the largest area is valid only if the area is greater than 300 to filter out the noise
                    area_max_contour = c

        return area_max_contour, contour_area_max


if __name__ == '__main__':
    p = ColorTracker()
    my_camera = Camera.Camera() 
    my_camera.camera_open()
    while True:
        img = my_camera.frame
        if img is not None:
            frame = p.detect_cube_center(img)
            cv2.imshow('Frame', frame)
            key = cv2.waitKey(1)
            if key == 27:
                break 
    my_camera.camera_close()
    cv2.destroyAllWindows()