'''
Created on Jan 8, 2017

@author: Kenny
'''

from robotpy_ext.autonomous import StatefulAutonomous, timed_state

class Dead_Reckoning_Gear(StatefulAutonomous):
    MODE_NAME = "Dead Reckoning Gear Scoring"

    def initialize(self):
        pass
    
    @timed_state(duration=15, first=True)
    def first(self):
        pass