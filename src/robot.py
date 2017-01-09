#!/usr/bin/env python3

import wpilib
import magicbot
#from components import vision
from robotpy_ext.common_drivers.navx.ahrs import AHRS

class MyRobot(magicbot.MagicRobot):
    #vision = vision.Vision
    def createObjects(self):
        self.navx = AHRS.create_spi()
    def teleopPeriodic(self):
        pass
if __name__ == "__main__":
    wpilib.run(MyRobot)
