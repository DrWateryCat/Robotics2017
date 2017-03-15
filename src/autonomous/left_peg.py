'''
Created on Mar 10, 2017

@author: Kenny
'''

from robotpy_ext.autonomous import *
from components import drive

class Left_Peg(StatefulAutonomous):
    MODE_NAME = "Left Peg"
    
    drive = drive.Drive

    def initialize(self):
        pass
    
    @state(first=True)
    def forwards(self, initial_call):
        if initial_call:
            self.drive.reset_encoders()
        if self.drive.drive_distance(58.5, speed=0.25):
            self.next_state("turn")
            
    @state
    def turn(self, initial_call):
        if initial_call:
            self.drive.reset()
            
        if self.drive.turn_to_angle(45, speed=0.25):
            self.next_state("approach")
            
    @state
    def approach(self, initial_call):
        if initial_call:
            self.drive.reset()
        
        
            