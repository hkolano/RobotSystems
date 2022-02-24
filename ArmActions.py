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
import logging


if sys.version_info.major == 2:
    print('Please run this program with python3!')
    sys.exit(0)


class ArmMover():

    def __init__(self):
        self.close_gripper_servo_value = 500
        self.AK = ArmIK() 

        self.range_rgb = {
            'red': (0, 0, 255),
            'blue': (255, 0, 0),
            'green': (0, 255, 0),
            'black': (0, 0, 0),
            'white': (255, 255, 255),
            }

    def go_to_initial_position(self):
        logging.info("Moving arm to initial position.")
        Board.setBusServoPulse(1, self.close_gripper_servo_value - 50, 300)
        Board.setBusServoPulse(2, 500, 500)
        self.AK.setPitchRangeMoving((0, 10, 10), -30, -30, -90, 1500)

    def set_lights_to_color(self, color=None):
        print(self.range_rgb[color])
        if color is not None:
            Board.RGB.setPixelColor(0, Board.PixelColor(self.range_rgb[color]))
            Board.RGB.setPixelColor(1, Board.PixelColor(self.range_rgb[color]))
        else:
            Board.RGB.setPixelColor(0, Board.PixelColor(0, 0, 0))
            Board.RGB.setPixelColor(1, Board.PixelColor(0, 0, 0))

        Board.RGB.show()        


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    m = ArmMover()
    m.go_to_initial_position()
    m.set_lights_to_color("red")