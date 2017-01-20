'''
Created on Jan 12, 2017

@author: Kenny
'''

import wpilib
import ctre

class Drive:
    '''
    classdocs
    '''
    left_talon0 = ctre.CANTalon
    left_talon1 = ctre.CANTalon
    
    right_talon0 = ctre.CANTalon
    right_talon1 = ctre.CANTalon
    
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
        self.left_talon0.set(self.left)
        self.right_talon0.set(self.right)