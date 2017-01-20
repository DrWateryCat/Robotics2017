'''
Created on Jan 12, 2017

@author: Kenny
'''

import wpilib

class Drive:
    '''
    classdocs
    '''
    drive_controller = wpilib.RobotDrive
    
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
    
    def execute(self):
        self.drive_controller.tankDrive(self.left, self.right)