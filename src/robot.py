#!/usr/bin/env python3

import wpilib
import magicbot
from components import drive, climber, lights
from robotpy_ext.common_drivers.navx.ahrs import AHRS
from wpilib.smartdashboard import SmartDashboard
import ctre
from common import unifiedjoystick, encoder, ledstrip
from wpilib.driverstation import DriverStation
from wpilib.interfaces import PIDSource

class MyRobot(magicbot.MagicRobot):
    drive = drive.Drive
    climber = climber.Climber
    lights = lights.Lights
    
    def createObjects(self):
        #navx
        self.navx = AHRS.create_spi()
        self.navx.setPIDSourceType(PIDSource.PIDSourceType.kDisplacement)
        
        #Drivetrain
        self.left_talon0 = ctre.CANTalon(0)
        self.left_talon1 = ctre.CANTalon(1)
        
        self.right_talon0 = ctre.CANTalon(2)
        self.right_talon1 = ctre.CANTalon(3)
        
        #Set up talon slaves
        self.left_talon1.setControlMode(ctre.CANTalon.ControlMode.Follower)
        self.left_talon1.set(self.left_talon0.getDeviceID())
        
        self.right_talon1.setControlMode(ctre.CANTalon.ControlMode.Follower)
        self.right_talon1.set(self.right_talon0.getDeviceID())
        
        #Set talon feedback device
        self.left_talon0.setFeedbackDevice(ctre.CANTalon.FeedbackDevice.QuadEncoder)
        self.right_talon0.setFeedbackDevice(ctre.CANTalon.FeedbackDevice.QuadEncoder)
        
        #Set the Ticks per revolution in the talons
        self.left_talon0.configEncoderCodesPerRev(1440)
        self.right_talon0.configEncoderCodesPerRev(1440)
        
        #Reverse left talon
        self.left_talon0.setInverted(True)
        self.right_talon0.setInverted(False)
        
        #Climber
        self.climber_motor = wpilib.Spark(0)
        self.climber_2 = wpilib.Talon(1)
        
        #Sensors
        self.left_enc = encoder.Encoder(self.left_talon0)
        self.right_enc = encoder.Encoder(self.right_talon0, True)
        
        #Controls
        self.left_joystick = wpilib.Joystick(0)
        self.right_joystick = wpilib.Joystick(1)
        
        self.climber_joystick = wpilib.Joystick(2)
        
        self.buttons = unifiedjoystick.UnifiedJoystick([self.left_joystick, self.right_joystick])
        
        self.last_button_state = False
        
        #Bling
        self.leds = ledstrip.LEDStrip()
        
        #Autonomous Placement
        self.auto_positions = wpilib.SendableChooser()
        self.auto_positions.addDefault("Position 1", 1)
        self.auto_positions.addObject("Position 2", 2)
        self.auto_positions.addObject("Position 3", 3)
        
        SmartDashboard.putData("auto_position", self.auto_positions)
        
        #SD variables
        SmartDashboard.putNumber("Vision/Turn", 0)
        SmartDashboard.putBoolean("Reversed", True)
        
    def autonomous(self):
        magicbot.MagicRobot.autonomous(self)
        
    def teleopInit(self):
        SmartDashboard.putBoolean("time_running", True)
        SmartDashboard.putNumber("time_remaining", 215)
        
    def teleopPeriodic(self):
        self.update_sd()
        self.drive.tankdrive(self.left_joystick.getRawAxis(1), self.right_joystick.getRawAxis(1))
        
        if self.climber_joystick.getRawButton(3):
            self.climber.enable()
            self.climber.set(self.climber_joystick.getRawAxis(1))
            
        if self.buttons.getButton(11) and self.last_button_state is False:
            self.last_button_state = True
            SmartDashboard.putBoolean("Reversed", not self.drive.reversed)
            
        if not self.buttons.getButton(11) and self.last_button_state is True:
            self.last_button_state = False
        
    def disabledInit(self):
        SmartDashboard.putBoolean("time_running", False)
        SmartDashboard.putBoolean("run_vision", False)
        self.drive.reset_encoders()
        magicbot.MagicRobot.disabledInit(self)
        
    def update_sd(self):
        SmartDashboard.putBoolean("time_running", True)
        SmartDashboard.putNumber("time_remaining", DriverStation.getInstance().getMatchTime() - 15)
        
if __name__ == "__main__":
    wpilib.run(MyRobot)
