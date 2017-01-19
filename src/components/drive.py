'''
Created on Jan 12, 2017

@author: Kenny
'''

from ctre import cantalon
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
        pass
    
    def execute(self):
        pass