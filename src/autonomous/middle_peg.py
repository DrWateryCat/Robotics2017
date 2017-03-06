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
        
    @timed_state(duration=5, next_state='vision', first=True)
    def forward(self):
        self.drive.arcade_drive(0, self.forward_speed)
        
    @timed_state(duration=3, next_state='end')
    def vision(self, initial_call):
        if initial_call:
            self.drive.stop()
            SmartDashboard.putBoolean("run_vision", True)
            
        turn_value = SmartDashboard.getNumber("Vision/Turn", 0) * self.turn_to_peg_P
        self.drive.arcade_drive(turn_value, self.forward_speed)
        
    @state
    def end(self):
        self.drive.stop()