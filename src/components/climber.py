'''
Created on Jan 19, 2017

@author: Kenny
'''

import wpilib
from magicbot.magic_tunable import tunable
from wpilib.smartdashboard import SmartDashboard

class Climber(object):
    '''
    classdocs
    '''
    
    climber_motor = wpilib.Spark
    def __init__(self):
        self.level = 0
        self.x = 1
    
    def enable(self):
        self.level = SmartDashboard.getNumber("Climber Multiplier", 0.65)
        
    def set(self, x):
        self.x = x
        
    def disable(self):
        self.level = 0
        
    def execute(self):
        self.climber_motor.set(-abs(self.level * self.x))
        
        self.x = 0