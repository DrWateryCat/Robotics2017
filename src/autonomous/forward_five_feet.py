'''
Created on Jan 28, 2017

@author: Kenny
'''

from robotpy_ext.autonomous import *
from components import drive

class Forward_Five_Feet(StatefulAutonomous):
    MODE_NAME = "Forward Five Feet"
    
    drive = drive.Drive

    def initialize(self):
        pass
    
    @state(first=True)
    def forward(self, initial_call):
        if initial_call:
            self.drive.reset_encoders()
        if self.drive.drive_by_ticks(1440, speed=0.25):
            self.next_state('end')
    @state
    def end(self):
        self.drive.arcade_drive(0, 0)