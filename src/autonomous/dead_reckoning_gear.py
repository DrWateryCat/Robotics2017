'''
Created on Jan 8, 2017

@author: Kenny
'''

from robotpy_ext.autonomous import StatefulAutonomous, state
from components import drive
import wpilib

class Dead_Reckoning_Gear(StatefulAutonomous):
    MODE_NAME = "Dead Reckoning Gear Scoring"
    
    drive = drive.Drive

    def initialize(self):
        self.driver_station = wpilib.DriverStation.getInstance()
        self.alliance_location = self.driver_station.getLocation()
        
        self.register_sd_var('drive_forward_inches', 60)
        
    @state(first=True)
    def drive_five_feet(self):
        if self.drive.drive_distance(self.drive_forward_inches):
            if self.alliance_location == 1:
                self.next_state("turn_right")
            elif self.alliance_location == 2:
                self.next_state("middle")
            elif self.alliance_location == 3:
                self.next_state("turn_left")
    
    @state
    def turn_left(self):
        if self.drive.turn_to_angle(45):
            self.next_state('end')
    
    @state
    def turn_right(self):
        if self.drive.turn_to_angle(315):
            self.next_state('end')
    
    @state
    def middle(self):
        self.next_state('end')
    
    @state
    def end(self):
        self.drive.arcadeDrive(0, 0)