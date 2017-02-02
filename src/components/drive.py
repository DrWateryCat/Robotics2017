'''
Created on Jan 12, 2017

@author: Kenny
'''

import ctre
import math
from robotpy_ext.common_drivers import navx
from common import encoder
from wpilib.smartdashboard import SmartDashboard
from networktables.util import ntproperty
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
    
    def __init__(self):
        self.left = 0
        self.right = 0
        
        self.iErr = 0

        self.sd = NetworkTable.getTable("/SmartDashboard")
        
        #Turn to angle PI values
        self.turning_P = self.sd.getAutoUpdateValue("TurnToAngle/P", 0.03)
        self.turning_I = self.sd.getAutoUpdateValue("TurnToAngle/I", 0.0001)
        self.turning_limit = self.sd.getAutoUpdateValue("TurnToAngle/Turning Speed", 0.37)
        
        #Set up talon slaves
        self.left_talon1.setControlMode(ctre.CANTalon.ControlMode.Follower)
        self.left_talon1.set(self.left_talon0.getDeviceID())
        
        self.right_talon1.setControlMode(ctre.CANTalon.ControlMode.Follower)
        self.right_talon1.set(self.right_talon0.getDeviceID())
        
        #Set talon feedback device
        self.left_talon0.setFeedbackDevice(CANTalon.FeedbackDevice.QuadEncoder)
        self.right_talon0.setFeedbackDevice(CANTalon.FeedbackDevice.QuadEncoder)
        
        #Set the Ticks per revolution in the talons
        self.left_talon0.configEncoderCodesPerRev(self.TICKS_PER_REV)
        self.right_talon0.configEncoderCodesPerRev(self.TICKS_PER_REV)
        
        #self.left_talon0.setProfile(0)
        #self.right_talon0.setProfile(0)
        
    
    def tankdrive(self, left, right):
        self.left = left
        self.right = right
    
    def arcade_drive(self, x, y):
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
                
    def get_gyro_angle(self):
        return self.navx.getYaw()
    
    def reset_gyro(self):
        self.navx.reset()
        
    def reset_encoders(self):
        self.left_enc.zero()
        self.right_enc.zero()
                
    def drive_distance(self, inches, speed=0.25, initial_call=False):
        return self.drive_by_ticks(self._get_inches_to_ticks(inches), speed, initial_call)
    
    def drive_by_ticks(self, ticks, speed=0.5, initial_call=False):
        if initial_call:
            self.reset_encoders()
        offset = ticks - self.left_enc.get()
        SmartDashboard.putNumber("Ticks offset", offset)
        
        if abs(offset) > 1000:
            y = offset * 0.0001
            y = max(min(speed, y), -speed)
            self.arcade_drive(0, y)
            return False
        return True
    
    def turn_to_angle(self, angle, speed=0.5):
        #Inline PI controller
        
        offset = angle - self.get_gyro_angle()
        if abs(offset) > 3:
            self.iErr += offset
            x = offset * self.turning_P.value * self.turning_I.value * self.iErr
            x = max(min(self.turning_limit.value, x), -self.turning_limit.value)
            self.arcade_drive(x, 0)
            return False
        self.iErr = 0
        return True
    
    def get_compass(self):
        return self.navx.getCompassHeading()
    
    def _get_inches_to_ticks(self, inches):
        return inches * (self.INCHES_PER_REVOLUTION * self.TICKS_PER_REV)
    
    def _update_sd(self):
        SmartDashboard.putNumber("Left Encoder Position", self.left_talon0.getSpeed())
        SmartDashboard.putNumber("Right Encoder Position", self.right_talon0.getSpeed())
        SmartDashboard.putNumber("heading", self.get_gyro_angle())
    
    def execute(self):
        self.left_talon0.set(-self.left)
        self.right_talon0.set(self.right)
        
        #Reset left and right to 0
        self.left = 0
        self.right = 0

        #Update SD
        self._update_sd()