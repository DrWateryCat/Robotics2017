'''
Created on Jan 19, 2017

@author: Kenny
'''

import wpilib

class Climber(object):
    '''
    classdocs
    '''
    
    climber_motor = wpilib.Spark
    def __init__(self):
        self.level = 0
    
    def enable(self):
        self.level = -0.5
        
    def execute(self):
        self.climber_motor.set(self.level)