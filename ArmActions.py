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


if sys.version_info.major == 2:
    print('Please run this program with python3!')
    sys.exit(0)


class ArmMover():

    def __init__(self):
        self.close_gripper_servo_value = 500
        self.AK = ArmIK() 

        self.range_rgb = {
            'blue': (0, 0, 255),
            'red': (255, 0, 0),
            'green': (0, 255, 0),
            'black': (0, 0, 0),
            'white': (255, 255, 255),
            }

        self.coordinate = {
            'red':   (-15 + 0.5, 12 - 0.5, 1.5),
            'green': (-15 + 0.5, 6 - 0.5,  1.5),
            'blue':  (-15 + 0.5, 0 - 0.5,  1.5),
            }

    def go_to_initial_position(self):
        logging.info("Moving arm to initial position.")
        Board.setBusServoPulse(1, self.close_gripper_servo_value - 50, 300)
        Board.setBusServoPulse(2, 500, 500)
        self.AK.setPitchRangeMoving((0, 10, 10), -30, -30, -90, 1500)

    def set_lights_to_color(self, color=None):
        # print(self.range_rgb[color])
        if color is not None:
            Board.RGB.setPixelColor(0, Board.PixelColor(*self.range_rgb[color]))
            Board.RGB.setPixelColor(1, Board.PixelColor(*self.range_rgb[color]))
        else:
            Board.RGB.setPixelColor(0, Board.PixelColor(0, 0, 0))
            Board.RGB.setPixelColor(1, Board.PixelColor(0, 0, 0))

        Board.RGB.show()

    def check_if_reachable(self, coords):
        result = self.AK.setPitchRangeMoving((coords[0], coords[1], 7), -90, -90, 0)
        if result == False:
            return False
        else:
            return True

    def set_up_grasp(self, coords):
        servo2_angle = getAngle(*coords) #Calculate the angle by which the gripper needs to be rotated
        self.open_gripper()
        Board.setBusServoPulse(2, servo2_angle, 500)

    def open_gripper(self):
        Board.setBusServoPulse(1, self.close_gripper_servo_value - 280, 500)    

    def close_gripper(self):
        Board.setBusServoPulse(1, self.close_gripper_servo_value, 500)     


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    p = ColorTracker()
    m = ArmMover()
    m.go_to_initial_position()
    time.sleep(0.5)

    cube_locations = p.get_cube_locs()
    if m.check_if_reachable(cube_locations['red']):
        m.set_up_grasp(cube_locations['red'])
    # m.check_if_reachable(p.get['red'])
    
    # detected_blocks = p.get_detected_blocks()

    # my_camera = Camera.Camera() 
    # my_camera.camera_open()
    # while True:
    #     img = my_camera.frame
    #     if img is not None:
    #         frame = p.detect_cubes(img)
    #         cv2.imshow('Frame', frame)
    #         key = cv2.waitKey(1)
    #         if key == 27:
    #             break 
    # my_camera.camera_close()
    # cv2.destroyAllWindows()
    
