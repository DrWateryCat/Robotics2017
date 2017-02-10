'''
Created on Feb 8, 2017

@author: Kenny
'''

from robotpy_ext.autonomous import *
from wpilib.smartdashboard import SmartDashboard
from networktables.networktable import NetworkTable
from components import drive
import wpilib

class Vision_Gear(StatefulAutonomous):
    MODE_NAME = "Vision Gear"
    
    drive = drive.Drive

    def initialize(self):
        self.turn = NetworkTable.getTable("/SmartDashboard").getGlobalAutoUpdateValue("Vision/Turn", 0, True)
        self.station = wpilib.DriverStation.getInstance().getLocation()
        
    @state(first=True)
    def start(self, initial_call):
        if initial_call:
            self.drive.reset_encoders()
            
        if self.drive.drive_distance(60):
            self.next_state("turn")
            
    @state
    def turn(self, initial_call):
        if self.station is 1:
            if self.drive.turn_to_angle(45):
                self.next_state("track_peg")
        elif self.station is 2:
            self.next_state("track_peg")
        else:
            if self.drive.turn_to_angle(315):
                self.next_state("track_peg")
                
    @state
    def track_peg(self, state_tm):
        if not state_tm > 5:
            self.drive.arcade_drive(0.25, self.turn.value)
        self.drive.arcade_drive(0, 0)