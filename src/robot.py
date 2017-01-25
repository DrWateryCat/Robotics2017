#!/usr/bin/env python3

import wpilib
import magicbot
from components import drive, climber
from robotpy_ext.common_drivers.navx.ahrs import AHRS
from wpilib.smartdashboard import SmartDashboard
import ctre
from common import unifiedjoystick, encoder
from wpilib.driverstation import DriverStation

class MyRobot(magicbot.MagicRobot):
    #vision = vision.Vision
    drive = drive.Drive
    climber = climber.Climber
    
    def createObjects(self):
        #navx
        self.navx = AHRS.create_spi()
        
        #Drivetrain
        self.left_talon0 = ctre.CANTalon(0)
        self.left_talon1 = ctre.CANTalon(1)
        
        self.right_talon0 = ctre.CANTalon(2)
        self.right_talon1 = ctre.CANTalon(3)
        
        self.left_talon1.setControlMode(ctre.CANTalon.ControlMode.Follower)
        self.left_talon1.set(self.left_talon0.getDeviceID())
        
        self.right_talon1.setControlMode(ctre.CANTalon.ControlMode.Follower)
        self.right_talon1.set(self.right_talon0.getDeviceID())
        
        #Climber
        self.climber_motor = wpilib.Spark(0)
        
        #Sensors
        self.left_enc = encoder.Encoder(self.left_talon0)
        self.right_enc = encoder.Encoder(self.right_talon0, True)
        
        #Controls
        self.left_joystick = wpilib.Joystick(0)
        self.right_joystick = wpilib.Joystick(1)
        
        self.buttons = unifiedjoystick.UnifiedJoystick([self.left_joystick, self.right_joystick])
        
    def autonomous(self):
        magicbot.MagicRobot.autonomous(self)
        
    def teleopPeriodic(self):
        SmartDashboard.putBoolean("time_running", True)
        SmartDashboard.putNumber("time_remaining", DriverStation.getInstance().getMatchTime() - 15)
        SmartDashboard.putNumber("heading", self.navx.getFusedHeading())
        self.drive.tankdrive(self.left_joystick.getRawAxis(1), self.right_joystick.getRawAxis(1))
        
    def disabledInit(self):
        SmartDashboard.putBoolean("time_running", False)
        magicbot.MagicRobot.disabledInit(self)
        
if __name__ == "__main__":
    wpilib.run(MyRobot)
