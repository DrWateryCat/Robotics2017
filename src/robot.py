#!/usr/bin/env python3

import wpilib
import magicbot

class MyRobot(magicbot.MagicRobot):
    def createObjects(self):
        pass
    def teleopPeriodic(self):
        pass
if __name__ == "__main__":
    wpilib.run(MyRobot)
