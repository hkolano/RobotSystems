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
from ArmPerception import ColorTracker
from ArmActions import ArmMover

if sys.version_info.major == 2:
    print('Please run this program with python3!')
    sys.exit(0)

class Flight():

    def __init__(self):
        self.p = ColorTracker()
        self.m = ArmMover()

        self.blocks_detected = False

    def check_for_blocks(self):
        blocks = self.p.get_detected_blocks
        if blocks == False:
            self.blocks_detected = False 
        else:
            self.blocks_detected = True


if __name__ == "__main__":
    f = Flight()
    