'''
Created on Jan 28, 2017

@author: Kenny
'''

from robotpy_ext.autonomous import *
from components import drive

class Forward_Five_Feet(StatefulAutonomous):
    MODE_NAME = "Robot tests"
    
    drive = drive.Drive

    def initialize(self):
        pass
    
    @state(first=True)
    def forward(self, initial_call):
        if initial_call:
            self.drive.reset_encoders()
        if self.drive.pid_turn_to_angle(-45):
            self.next_state('end')
    @state
    def end(self):
        self.drive.arcade_drive(0, 0)