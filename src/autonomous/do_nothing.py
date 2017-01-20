'''
Created on Jan 19, 2017

@author: Kenny
'''

from robotpy_ext.autonomous import *

class Do_Nothing(StatefulAutonomous):
    MODE_NAME = "Do Nothing"

    def initialize(self):
        pass
    
    @state(first=True)
    def nothing(self):
        pass