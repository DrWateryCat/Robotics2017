from robotpy_ext.autonomous import *
from wpilib.smartdashboard import SmartDashboard
from networktables.networktable import NetworkTable
from components import drive
import wpilib
from magicbot.magic_tunable import tunable
import logging

class Vision_Gear(StatefulAutonomous):
    MODE_NAME = "Vision Gear"
    
    drive = drive.Drive

    def initialize(self):
        self.register_sd_var('initial_distance', 60, vmin=0, vmax=150)
        self.register_sd_var("middle_peg_distance", 24, vmin=1, vmax=100)
        self.register_sd_var('turning_time', 1.5, vmin=1, vmax=5)
        self.register_sd_var('turning_speed', 0.25)
        self.register_sd_var('turn_to_peg_P', 0.075)
        self.register_sd_var("wait_to_look", 0.5, vmin=0, vmax=3)
        self.register_sd_var("turn_left_angle", 300, vmin=0, vmax=360)
        self.register_sd_var("turn_right_angle", 60, vmin=0, vmax=360)
        self.register_sd_var("forward_time", 3, vmin=1, vmax=10)
        
        self.turnt = False
        self.found = False
        SmartDashboard.putBoolean("run_vision", False)
        
        self.logger = logging.Logger("Vision Auto")
        
    @state(first=True)
    def forwards(self, initial_call, state_tm):
        self.found = False
        SmartDashboard.putBoolean("Found", False)
        if initial_call:
            self.drive.reset_encoders()
            self.logger.info(SmartDashboard.getString("auto_position/selected"))
            
        if SmartDashboard.getString("auto_position/selected", "Position 1") is "Position 2":
            distance = self.middle_peg_distance
        else:
            distance = self.initial_distance
        if self.drive.drive_distance(distance, speed=0.25):
            self.drive.stop()
            self.next_state('turn')
                  
    @state
    def turn(self):
        station = SmartDashboard.getString("auto_position/selected", "Position 1")
        SmartDashboard.putBoolean("run_vision", False)
        if station is "Position 1":
            self.next_state('turn_right')
        elif station is "Position 3":
            self.next_state('turn_left')
        else:
            self.next_state('approach')
            
    @state
    def turn_left(self, state_tm, initial_call):
        if initial_call:
            self.drive.reset_encoders()
            
        if SmartDashboard.getDouble("angle_offset") < (self.turn_left_angle / 2):
            SmartDashboard.putBoolean("run_vision", True)
            
        if self.drive.turn_to_angle(self.turn_left_angle):
            self.next_state('approach')
    
    @state
    def turn_right(self, state_tm, initial_call):
        """
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
                self.drive.tankdrive(-self.turning_speed, self.turning_speed)
                
        SmartDashboard.putBoolean("Found", self.found)"""
        if initial_call:
            self.drive.reset_encoders()
        if SmartDashboard.getDouble("angle_offset") < (self.turn_right_angle / 2):
            SmartDashboard.putBoolean("run_vision", True)
        if self.drive.turn_to_angle(self.turn_right_angle):
            self.next_state('approach')

        
    @timed_state(duration=3, next_state='stop')
    def found_hook(self):
        turning_amt = SmartDashboard.getNumber("Vision/Turn", 0) * self.turn_to_peg_P
        self.drive.arcade_drive(turning_amt, 0.2)
          
    @state
    def approach(self, state_tm):
        if SmartDashboard.getBoolean("Vision/Found Hook"):
            self.next_state('found_hook')
        else:
            if state_tm < self.forward_time:
                self.drive.arcade_drive(0, 0.25)
            else:
                self.next_state('stop')
    
    @state
    def stop(self):
        self.drive.stop()
        