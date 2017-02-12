from robotpy_ext.autonomous import *
from wpilib.smartdashboard import SmartDashboard
from networktables.networktable import NetworkTable
from components import drive
import wpilib
from magicbot.magic_tunable import tunable

class Vision_Gear(StatefulAutonomous):
    MODE_NAME = "Vision Gear"
    
    drive = drive.Drive

    def initialize(self):
        self.register_sd_var('initial_distance', 93, vmin=0, vmax=150)
        self.register_sd_var('turning_time', 3, vmin=1, vmax=5)
        self.register_sd_var('turning_speed', 0.25)
        self.register_sd_var('turn_to_peg_P', 0.005)
        
        self.turnt = False #turnt AF
        
    @state(first=True)
    def forwards(self, initial_call):
        if initial_call:
            self.drive.reset_encoders()
        if self.drive.drive_distance(self.initial_distance):
            self.drive.stop()
            self.next_state('turn')
            
    @state
    def turn(self):
        station = wpilib.DriverStation.getInstance().getLocation()
        if station is 1:
            self.next_state('turn_right')
        elif station is 3:
            self.next_state('turn_left')
        else:
            self.next_state('straight')
            
    @state
    def turn_left(self, state_tm):
        if SmartDashboard.getBoolean('Vision/Found Hook', False):
            self.drive.stop()
            self.next_state('found_peg')
        else:
            if state_tm > self.turning_time:
                if not self.turnt:
                    self.turnt = True
                    self.next_state('turn_right')
                else:
                    self.next_state('stop')
            else:
                self.drive.arcade_drive(-(self.turning_speed), 0)
    
    @state
    def turn_right(self, state_tm):
        if SmartDashboard.getBoolean('Vision/Found Hook', False):
            self.drive.stop()
            self.next_state('found_peg')
        else:
            if state_tm > self.turning_time:
                if not self.turnt:
                    self.turnt = True
                    self.next_state('turn_left')
                else:
                    self.next_state('stop')
            else:
                self.drive.arcade_drive(self.turning_speed, 0)
        
    @timed_state(duration=3, next_state='stop')
    def found_peg(self):
        turning_amt = SmartDashboard.getNumber("Vision/Turn", 0) * self.turn_to_peg_P
        self.drive.arcade_drive(turning_amt, 0.25)
    
    @state
    def straight(self, state_tm):
        self.next_state('stop')
    
    @state
    def stop(self):
        self.drive.stop()