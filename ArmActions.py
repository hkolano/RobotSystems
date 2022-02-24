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
from logdecorator import log_on_start , log_on_end , log_on_error


if sys.version_info.major == 2:
    print('Please run this program with python3!')
    sys.exit(0)


class ArmMover():

    def __init__(self):
        self.close_gripper_servo_value = 500
        self.AK = ArmIK() 

    def go_to_initial_position(self):
        Board.setBusServoPulse(1, self.close_gripper_servo_value - 50, 300)
        Board.setBusServoPulse(2, 500, 500)
        self.AK.setPitchRangeMoving((0, 10, 10), -30, -30, -90, 1500)
        


if __name__ == "__main__":
    m = ArmMover()
    m.go_to_initial_position()