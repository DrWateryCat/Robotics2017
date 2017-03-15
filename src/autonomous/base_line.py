'''
Created on Jan 23, 2017

@author: Kenny
'''

from robotpy_ext.autonomous import *
from components import drive

class Base_Line(StatefulAutonomous):
    MODE_NAME = "Base line"
    
    drive = drive.Drive

    def initialize(self):
        pass
    
    @timed_state(duration=7, next_state='stop', first=True)
    def forward(self):
        self.drive.drive_straight()
        
    @state
    def stop(self):
        self.drive.stop()