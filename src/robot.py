#!/usr/bin/env python3

import wpilib
import magicbot
from components import drive, climber, sensor
from robotpy_ext.common_drivers.navx.ahrs import AHRS
from robotpy_ext.common_drivers import xl_max_sonar_ez
from wpilib.smartdashboard import SmartDashboard
import ctre
from common import unifiedjoystick, encoder
from wpilib.driverstation import DriverStation

class MyRobot(magicbot.MagicRobot):
    drive = drive.Drive
    climber = climber.Climber
    sensors = sensor.Sensor
    
    def createObjects(self):
        #navx
        self.navx = AHRS.create_spi()
        
        #Drivetrain
        self.left_talon0 = ctre.CANTalon(0)
        self.left_talon1 = ctre.CANTalon(1)
        
        self.right_talon0 = ctre.CANTalon(2)
        self.right_talon1 = ctre.CANTalon(3)
        
        #Climber
        self.climber_motor = wpilib.Spark(0)
        
        #Sensors
        self.left_enc = encoder.Encoder(self.left_talon0)
        self.right_enc = encoder.Encoder(self.right_talon0, True)
        
        self.sonar = xl_max_sonar_ez.MaxSonarEZAnalog(0)
        
        #Controls
        self.left_joystick = wpilib.Joystick(0)
        self.right_joystick = wpilib.Joystick(1)
        
        self.buttons = unifiedjoystick.UnifiedJoystick([self.left_joystick, self.right_joystick])
        
    def autonomous(self):
        magicbot.MagicRobot.autonomous(self)
        
    def teleopPeriodic(self):
        self.update_sd()
        self.drive.tankdrive(self.left_joystick.getRawAxis(1) * 0.75, self.right_joystick.getRawAxis(1) * 0.75)
        
    def disabledInit(self):
        SmartDashboard.putBoolean("time_running", False)
        self.drive.reset_encoders()
        magicbot.MagicRobot.disabledInit(self)

    def update_sd(self):
        SmartDashboard.putBoolean("time_running", True)
        SmartDashboard.putNumber("time_remaining", DriverStation.getInstance().getMatchTime() - 15)
        
        
        
if __name__ == "__main__":
    wpilib.run(MyRobot)
