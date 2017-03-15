'''
Created on Mar 5, 2017

@author: Kenny
'''

from robotpy_ext.autonomous import *
from components import drive
from wpilib.smartdashboard import SmartDashboard

class Middle_Gear(StatefulAutonomous):
    MODE_NAME = "Middle Gear"
    
    drive = drive.Drive

    def initialize(self):
        self.register_sd_var("turn_to_peg_P", 0.075, vmin=0, vmax=1)
        self.register_sd_var("forward_speed", 0.25, vmin=-1, vmax=1)
        
    @state(first=True)
    def forward(self, initial_call):
        if initial_call:
            self.drive.reset_encoders()
        if self.drive.drive_distance(52.3, speed=self.forward_speed):
            self.next_state("end")
        
    @state
    def end(self):
        self.drive.stop()