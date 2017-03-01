'''
Created on Jan 12, 2017

@author: Kenny
'''

import ctre
from robotpy_ext.common_drivers import navx
from common import encoder
from wpilib.smartdashboard import SmartDashboard
from networktables import NetworkTable
from ctre.cantalon import CANTalon

class Drive:
    '''
    classdocs
    '''
    #Motors
    left_talon0 = ctre.CANTalon
    left_talon1 = ctre.CANTalon
    
    right_talon0 = ctre.CANTalon
    right_talon1 = ctre.CANTalon
    
    #Sensors
    navx = navx.AHRS
    left_enc = encoder.Encoder
    right_enc = encoder.Encoder
    
    #Constants
    TICKS_PER_REV = 1440
    WHEEL_DIAMETER = 6
    GEAR_RATIO = 10.71
    INCHES_PER_REVOLUTION = 18.84
    TICKS_PER_INCH = 76.433
    
    def __init__(self):
        self.left = 0
        self.right = 0
        
        self.pid_angle = 0

        self.sd = NetworkTable.getTable("/SmartDashboard")
        
        #Turn to angle PI values
        self.turning_P = self.sd.getAutoUpdateValue("TurnToAngle/P", 0.03)
        #self.turning_I = self.sd.getAutoUpdateValue("TurnToAngle/I", 0.0001)
        #self.turning_D = self.sd.getAutoUpdateValue("TurnToAngle/D", 0.001)
        self.turning_limit = self.sd.getAutoUpdateValue("TurnToAngle/Turning Speed", 0.37)
        
        self.drive_constant = self.sd.getAutoUpdateValue("Drive/Drive Constant", 0.0001)
        self.drive_multiplier = self.sd.getAutoUpdateValue("Drive/Drive Multiplier", 0.75)
        
        SmartDashboard.putBoolean("Reversed", False)
        
        self.reversed = False
    
    def tankdrive(self, left, right):
        self.left = left
        self.right = right
        
        self._set_talon_to_throttle_mode()
    
    def arcade_drive(self, x, y):
        self._set_talon_to_throttle_mode()
        if y > 0.0:
            if x > 0.0:
                self.left = y - x
                self.right = max(y, x)
            else:
                self.left = max(y, -x)
                self.right = x + y
        else:
            if x > 0.0:
                self.left = -max(-y, x)
                self.right = y + x
            else:
                self.left = y - x
                self.right = -max(-y, -x)
                
    def turn_in_place(self, speed):
        self._set_talon_to_throttle_mode()
        
        self.left = speed
        self.right = -speed
    def reverse(self):
        SmartDashboard.putBoolean("Reversed", not SmartDashboard.getBoolean("Reversed", False))
                
    def get_gyro_angle(self):
        return self.navx.getYaw()
    
    def reset_gyro(self):
        self.navx.reset()
        
    def reset_encoders(self):
        self.left_talon0.setEncPosition(0)
        self.right_talon0.setEncPosition(0)
                
    def drive_distance(self, inches, speed=0.1):
        return self.drive_by_ticks(self._get_inches_to_ticks(inches), speed)
    
    def drive_by_ticks(self, ticks, speed=0.1):
        offset = self.left_talon0.getEncPosition() - ticks
        SmartDashboard.putNumber("Offset", offset)
        if abs(offset) > 50:
            self.arcade_drive(0, speed)
            return False
        self.stop()
        return True
    
    def turn_to_angle(self, angle, speed=0.5):
        offset = angle - self.get_gyro_angle()
        
        if abs(offset) > 3:
            p = self.turning_P.value * offset
            value = max(min(self.turning_limit.value, p), -self.turning_limit.value)
            self.arcade_drive(value, 0)
            return False
        return True
    
    def get_compass(self):
        return self.navx.getCompassHeading()
    
    def _get_inches_to_ticks(self, inches):
        return inches * self.TICKS_PER_INCH
    
    def _update_sd(self):
        SmartDashboard.putNumber("Left Encoder Position", self.left_talon0.getEncPosition())
        SmartDashboard.putNumber("Right Encoder Position", self.right_talon0.getEncPosition())
        SmartDashboard.putNumber("heading", self.get_gyro_angle())
        self.reversed = SmartDashboard.getBoolean("Reversed", False)
        
    def _set_talon_to_position_mode(self):
        self.left_talon0.changeControlMode(CANTalon.ControlMode.Position)
        self.right_talon0.changeControlMode(CANTalon.ControlMode.Position)
        
    def _set_talon_to_throttle_mode(self):
        self.left_talon0.changeControlMode(CANTalon.ControlMode.PercentVbus)
        self.right_talon0.changeControlMode(CANTalon.ControlMode.PercentVbus)
        
    def _set_talon_position(self, position):
        self._set_talon_to_position_mode()
        self.left_talon0.set(position)
        self.right_talon0.set(position)
        
    def get_encoder_ticks(self):
        return self.left_enc.get()
    
    def get_distance_since_reset(self):
        return (self.get_distance_since_reset() / self.TICKS_PER_REV) / self.INCHES_PER_REVOLUTION
    
    def stop(self):
        self.arcade_drive(0, 0)
    
    def execute(self):
        if self.reversed:
            self.left_talon0.set(-self.right * self.drive_multiplier.value)
            self.right_talon0.set(-self.left * self.drive_multiplier.value)
        else:
            #0.94375
            self.left_talon0.set(self.left * self.drive_multiplier.value)
            self.right_talon0.set(self.right * self.drive_multiplier.value)
        
        #Reset left and right to 0
        self.left = 0
        self.right = 0

        #Update SD
        self._update_sd()