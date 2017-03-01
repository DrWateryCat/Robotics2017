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
        self.register_sd_var('initial_distance', 60, vmin=0, vmax=150)
        self.register_sd_var("forward_time", 4, vmin=1, vmax=5)
        self.register_sd_var('turning_time', 1.5, vmin=1, vmax=5)
        self.register_sd_var('turning_speed', 0.25)
        self.register_sd_var('turn_to_peg_P', 0.075)
        self.register_sd_var("wait_to_look", 0.5, vmin=0, vmax=3)
        
        self.turnt = False #turnt AF
        self.found = False
        SmartDashboard.putBoolean("run_vision", False)
        
    @state(first=True)
    def forwards(self, initial_call, state_tm):
        self.found = False
        SmartDashboard.putBoolean("Found", False)
        if initial_call:
            self.drive.reset_encoders()
        if self.drive.drive_distance(self.initial_distance, speed=0.25) or state_tm > self.forward_time:
            self.drive.stop()
            self.next_state('turn')
            
            
    @state
    def turn(self):
        station = wpilib.DriverStation.getInstance().getLocation()
        SmartDashboard.putBoolean("run_vision", False)
        if station is 1:
            self.next_state('turn_right')
        elif station is 3:
            self.next_state('turn_left')
        else:
            self.next_state('straight')
            
    @state
    def turn_left(self, state_tm):
        if SmartDashboard.getBoolean("Vision/Found Hook", False):
            self.found = True
        
        if state_tm > self.wait_to_look:
            if SmartDashboard.getBoolean("Vision/Found Hook", False):
                self.found = True
            SmartDashboard.putBoolean("run_vision", True)
            if self.found:
                self.drive.stop()
                self.next_state('found_hook')
            else:
                self.drive.stop()
                self.next_state('stop')
        else:
            if SmartDashboard.getBoolean("Vision/Found Hook", False):
                self.found = True
            if state_tm > self.turning_time:
                if not self.turnt:
                    self.turnt = True
                    self.next_state('turn_right')
                else:
                    self.next_state('stop')
            else:
                self.drive.tankdrive(self.turning_speed, -self.turning_speed)
                
        SmartDashboard.putBoolean("Found", self.found)
    
    @state
    def turn_right(self, state_tm):
        if SmartDashboard.getBoolean("Vision/Found Hook", False):
            self.found = True
        
        if state_tm > self.turn_to_look:
            if SmartDashboard.getBoolean("Vision/Found Hook", False):
                self.found = True
            if self.found:
                self.found = True
                self.drive.stop()
                self.next_state('found_hook')
            else:
                self.drive.stop()
                self.next_state('stop')
        else:
            if SmartDashboard.getBoolean("Vision/Found Hook", False):
                self.found = True
            if state_tm > self.turning_time:
                if not self.turnt:
                    self.turnt = True
                    self.next_state('turn_left')
                else:
                    self.next_state('stop')
            else:
                self.drive.tankdrive(-self.turning_speed, self.turning_speed)
                
        SmartDashboard.putBoolean("Found", self.found)

        
    @timed_state(duration=3, next_state='stop')
    def found_hook(self):
        turning_amt = SmartDashboard.getNumber("Vision/Turn", 0) * self.turn_to_peg_P
        self.drive.arcade_drive(turning_amt, 0.2)
    
    @state
    def straight(self, state_tm):
        self.next_state('stop')
    
    @state
    def stop(self):
        self.drive.stop()
        if SmartDashboard.getBoolean("Vision/Found Hook", False) and self.found is not True:
            self.found = True
            self.next_state('found_hook')
        