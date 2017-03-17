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
import wpilib
from wpilib.interfaces.pidsource import PIDSource
import hal
import logging

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
    
    def setup(self):
        self.left = 0
        self.right = 0

        self.sd = NetworkTable.getTable("/SmartDashboard")
        
        #Turn to angle PI values
        self.turning_P = self.sd.getAutoUpdateValue("TurnToAngle/P", 1)
        self.turning_I = self.sd.getAutoUpdateValue("TurnToAngle/I", 0)
        self.turning_D = self.sd.getAutoUpdateValue("TurnToAngle/D", 0)
        
        self.turn_controller = wpilib.PIDController(Kp=self.turning_P.value, Ki=self.turning_I.value, Kd=self.turning_D.value, source=self, output=self)
        self.turn_controller.setInputRange(-180, 180)
        self.turn_controller.setOutputRange(-1, 1)
        self.turn_controller.setContinuous(True)
        
        self.pid_value = 0
        
        self.drive_constant = self.sd.getAutoUpdateValue("Drive/Drive Constant", 0.0001)
        self.drive_multiplier = self.sd.getAutoUpdateValue("Drive/Drive Multiplier", 0.75)
        
        SmartDashboard.putBoolean("Reversed", False)
        
        self.reversed = False
        
        self.logger = logging.getLogger("drive")
        
        self.iErr = 0
    
    def tankdrive(self, left, right):
        self.left = left
        self.right = right
        
        self._set_talon_to_throttle_mode()
    
    def arcade_drive(self, x, y):
        self._set_talon_to_throttle_mode()
        if y > 0.0:
            if x > 0.0:
                self.left = y - x
                self.right = max(y, x) * 0.94375
            else:
                self.left = max(y, -x)
                self.right = x + y  * 0.94375
        else:
            if x > 0.0:
                self.left = -max(-y, x)
                self.right = y + x * 0.94375
            else:
                self.left = y - x
                self.right = -max(-y, -x) * 0.94375
                
    def drive_straight(self, speed=0.25):
        self.turn_controller.enable()
        #Stay straight
        self.turn_controller.setSetpoint(0)
        if not hal.isSimulation():
            self.arcade_drive(self.pid_value, speed)
        else:
            self.arcade_drive(0, speed)
                
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
        
    def reset(self):
        self.reset_encoders()
        self.reset_gyro()
                
    def drive_distance(self, inches, speed=0.25):
        return self.drive_by_ticks(self._get_inches_to_ticks(inches), speed)
    
    def drive_by_ticks(self, ticks, speed=0.25):
        offset = ticks - self.get_encoder_ticks()
        SmartDashboard.putNumber("Offset", offset)
        if abs(offset) > 50:
            self.arcade_drive(0, speed)
            return False
        self.stop()
        return True
    
    def turn_to_angle(self, angle, speed=0.25):
        offset = angle - self.get_gyro_angle()
        SmartDashboard.putDouble("angle_offset", offset)
        if abs(offset) > 0.1:
            if offset > 0:
                turn_speed = speed
            else:
                turn_speed = -speed
            self.arcade_drive(turn_speed, speed)
            return False
        return True
    
    def pid_turn_to_angle(self, angle, speed=0.25):
        offset = angle - self.get_gyro_angle()
        SmartDashboard.putNumber("angle_offset", offset)
        if abs(offset) > 2:
            self.iErr += offset
            
            turn = (offset * self.turning_P.value) + (self.turning_I.value * self.iErr)
            turn = max(min(speed, turn), -speed)
            
            if angle < 0:
                #Negative angle, negative turn
                turn = abs(turn)
            else:
                turn = -abs(turn)
            
            SmartDashboard.putNumber('turn_value', turn)
            self.arcade_drive(turn, 0)
            return False
        self.logger.info("Turned to angle " + str(angle))
        self.iErr = 0
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
        
        self.turn_controller.setPID(self.turning_P.value, self.turning_I.value, self.turning_D.value, 0)
        
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
        return self.right_talon0.getPosition()
    
    def get_distance_since_reset(self):
        return (self.get_distance_since_reset() / self.TICKS_PER_REV) / self.INCHES_PER_REVOLUTION
    
    def stop(self):
        self.arcade_drive(0, 0)
    
    def execute(self):
        if self.reversed:
            self.left_talon0.set(-self.right * self.drive_multiplier.value)
            if hal.isSimulation():
                self.right_talon0.set(-self.left * self.drive_multiplier.value)
            else:
                self.right_talon0.set(-self.left * self.drive_multiplier.value)
        else:
            #0.94375
            self.left_talon0.set(self.left * self.drive_multiplier.value)
            if hal.isSimulation():
                self.right_talon0.set(self.right * self.drive_multiplier.value)
            else:
                self.right_talon0.set(self.right * self.drive_multiplier.value)
        
        #Reset left and right to 0
        self.left = 0
        self.right = 0

        #Update SD
        self._update_sd()
        
    def pidGet(self):
        return self.get_gyro_angle()
    
    def getPIDSourceType(self):
        return PIDSource.PIDSourceType.kDisplacement
    
    def pidWrite(self, val):
        self.pid_value = val