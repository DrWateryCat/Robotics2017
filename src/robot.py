#!/usr/bin/env python3

import wpilib
import magicbot
#from components import vision
from robotpy_ext.common_drivers.navx.ahrs import AHRS
from wpilib.smartdashboard import SmartDashboard

class MyRobot(magicbot.MagicRobot):
    #vision = vision.Vision
    def createObjects(self):
        self.navx = AHRS.create_spi()
    def teleopPeriodic(self):
        SmartDashboard.putNumber("Heading", self.navx.getFusedHeading())
if __name__ == "__main__":
    wpilib.run(MyRobot)
