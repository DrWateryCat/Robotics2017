'''
Created on Jan 12, 2017

@author: Kenny
'''

import ctre
import math

class Drive:
    '''
    classdocs
    '''
    left_talon0 = ctre.CANTalon
    left_talon1 = ctre.CANTalon
    
    right_talon0 = ctre.CANTalon
    right_talon1 = ctre.CANTalon
    
    TICKS_PER_REV = 1440
    WHEEL_DIAMETER = 6
    GEAR_RATIO = 10.71
    
    def __init__(self):
        self.left = 0
        self.right = 0
    
    def tankdrive(self, left, right):
        self.left = left
        self.right = right
    
    def arcade_drive(self, x, y):
        if y > 0.0:
            if x > 0.0:
                self.left = y - x
                self.right = max(y, x)
            else:
                self.left = max(y, -x)
                self.right = x + y
        else:
            if x > 0.0:
                self.left = -max(-y, x)
                self.right = y + x
            else:
                self.left = y - x
                self.right = -max(-y, -x)
                
    def drive_distance(self, inches, speed=0.5):
        return self.drive_by_ticks(self._get_inches_to_ticks(inches), speed)
    
    def drive_by_ticks(self, ticks, speed=0.5):
        offset = ticks - self.get_encoder_position()
        
        if abs(offset) > 1000:
            y = offset * 0.0001
            y = max(min(speed, y), -speed)
            self.arcade_drive(0, y)
            return False
        return True
    
    def _get_inches_to_ticks(self, inches):
        return ((self.GEAR_RATIO * self.TICKS_PER_REV * inches) / (math.pi*self.WHEEL_DIAMETER))
    
    def execute(self):
        self.left_talon0.set(self.left)
        self.right_talon0.set(self.right)