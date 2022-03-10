#!/usr/bin/python3
# coding=utf8
import sys

from numpy import square
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
        self.AK = ArmIK()
        self.gripper_vals = {
            'cube': 500,
            'open': 220
        } 

        self.heights = {
            'cube': {
                'above':7,
                'ground':1.5,
                'drop':4.5
            },
            'wall': {
                'above': 12
            }
        }

        self.range_rgb = {
            'blue': (0, 0, 255),
            'red': (255, 0, 0),
            'green': (0, 255, 0),
            'black': (0, 0, 0),
            'white': (255, 255, 255),
            }

        # Coordinates of colored boxes on mat
        self.coordinate = {
            'red':   (-15 + 0.5, 12 - 0.5, 1.5),
            'green': (-15 + 0.5, 6 - 0.5,  1.5),
            'blue':  (-15 + 0.5, 0 - 0.5,  1.5),
            }

    def go_to_initial_position(self):
        logging.info("Moving arm to initial position.")
        self.open_gripper()
        time.sleep(1.0)
        Board.setBusServoPulse(2, 500, 500)
        self.AK.setPitchRangeMoving((0, 10, 10), -30, -30, -90, 1500)
        time.sleep(1.5)

    def set_lights_to_color(self, color=None):
        # print(self.range_rgb[color])
        if color is not None:
            Board.RGB.setPixelColor(0, Board.PixelColor(*self.range_rgb[color]))
            Board.RGB.setPixelColor(1, Board.PixelColor(*self.range_rgb[color]))
        else:
            Board.RGB.setPixelColor(0, Board.PixelColor(0, 0, 0))
            Board.RGB.setPixelColor(1, Board.PixelColor(0, 0, 0))

        Board.RGB.show()

    def check_if_reachable(self, coords, object):
        # print("Checking if coords {} is reachable".format(coords))
        # result = self.AK.setPitchRangeMoving((coords[0], coords[1], 7), -90, -90, 0)
        result = self.AK.setPitchRangeMoving((coords[0], coords[1], self.heights[object]['ground']), -90, -90, 0)
        if result == False:
            # print("not reachable.")
            return False
        else:
            # print("reachable!")
            return True
        # time.sleep(result[2]/1000)

    def move_to_coords(self, x, y, height, duration=1.5):
        '''Moves gripper to location provided
        optional input: duration of movement'''
        self.AK.setPitchRangeMoving((x, y, height), -90, -90, 0)
        time.sleep(duration)

    def set_gripper_angle(self, angle):
        Board.setBusServoPulse(2, angle, 500)
        time.sleep(0.8)

    def grasp_obj_at_coords(self, coords, object):
        '''Picks up the object located at the coordinates given'''
        # move to above the object and open the gripper
        self.move_to_coords(coords[0], coords[1], self.heights[object]['above'])
        self.open_gripper()
        # Set the gripper angle
        gripper_angle = getAngle(*coords) #Calculate the angle by which the gripper needs to be rotated
        self.set_gripper_angle(gripper_angle)
        # Lower to around cube
        self.move_to_coords(coords[0], coords[1], self.heights[object]['ground'])
        self.close_gripper(object)
        self.move_to_coords(coords[0], coords[1], self.heights[object]['above'])

    def drop_cube_in_square(self, square_color):
        loc = self.coordinate[square_color]
        self.drop_obj_in_loc(loc, 'cube')

    def drop_obj_in_loc(self, loc, object):
        '''Places an (already grasped) object in a location'''
        # move to location over object
        self.move_to_coords(loc[0], loc[1], self.heights[object]['above'])
        # set the angle to be straight
        straight_angle = getAngle(loc[0], loc[1], -90)
        self.set_gripper_angle(straight_angle)

        # drop object
        self.move_to_coords(loc[0], loc[1], self.heights[object]['drop'], duration=0.5)
        self.open_gripper()
        self.move_to_coords(loc[0], loc[1], self.heights[object]['above'], duration=0.8)

    def open_gripper(self):
        Board.setBusServoPulse(1, self.gripper_vals['open'], 500)
        time.sleep(0.8)    

    def close_gripper(self, object):
        Board.setBusServoPulse(1, self.gripper_vals[object], 500)     
        time.sleep(0.8)


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    p = ColorTracker()
    m = ArmMover()
    m.go_to_initial_position()
    time.sleep(0.5)    
    # detected_blocks = p.get_detected_blocks()

    
