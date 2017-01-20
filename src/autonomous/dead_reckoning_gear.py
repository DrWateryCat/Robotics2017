'''
Created on Jan 8, 2017

@author: Kenny
'''

from robotpy_ext.autonomous import StatefulAutonomous, timed_state, state
import wpilib

class Dead_Reckoning_Gear(StatefulAutonomous):
    MODE_NAME = "Dead Reckoning Gear Scoring"

    def initialize(self):
        self.driver_station = wpilib.DriverStation.getInstance()
        self.alliance_location = self.driver_station.getLocation()
        
    @state(first=True)
    def drive_five_feet(self):
        if self.drive.drive_distance(60):
            if self.alliance_location == 1:
                self.next_state("turn_right")
            elif self.alliance_location == 2:
                self.next_state("middle")
            elif self.alliance_location == 3:
                self.next_state("turn_left")
    
    @state
    def turn_left(self):
        pass
    
    @state
    def turn_right(self):
        pass
    
    @state
    def middle(self):
        pass
    
    @state
    def end(self):
        self.drive.arcadeDrive(0, 0)