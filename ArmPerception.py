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
        self.get_roi = False

        self.range_rgb = {
            'red': (0, 0, 255),
            'blue': (255, 0, 0),
            'green': (0, 255, 0),
            'black': (0, 0, 0),
            'white': (255, 255, 255),
            }

    def detect_cube_center(self, img):
        self.prepare_image(img)
        red_mask, area_redmaxcontour, area_redmax = self.detect_color_contours('red')
        if area_redmax > 2500:
            self.get_bounding_box(area_redmaxcontour, 'red')
        return self.og_img

    def prepare_image(self, img):
        self.og_img = img 
        self.img_copy = img.copy()
        self.img_h, self.img_w = img.shape[:2]

        # Draw the center line
        cv2.line(img, (0, int(img_h / 2)), (img_w, int(img_h / 2)), (0, 0, 200), 1)
        cv2.line(img, (int(img_w / 2), 0), (int(img_w / 2), img_h), (0, 0, 200), 1)
        
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
        return closed, areaMaxContour, area_max

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

    def get_bounding_box(self, contour, color):
        rect = cv2.minAreaRect(contour)
        box = np.int0(cv2.boxPoints(rect))

        roi = getROI(box)
        self.get_roi = True

        img_centerx, img_centery = getCenter(rect, roi, self.img_size, square_length)  # 获取木块中心坐标 get the coordinates of the center of the block
        world_x, world_y = convertCoordinate(img_centerx, img_centery, self.img_size) #转换为现实世界坐标 convert to real world coordinates
        
        # draw box and middle point
        cv2.drawContours(self.og_img, [box], -1, self.range_rgb[color], 2)
        cv2.putText(self.og_img, '(' + str(world_x) + ',' + str(world_y) + ')', (min(box[0, 0], box[2, 0]), box[2, 1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.range_rgb[color], 1) #绘制中心点 draw center point


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