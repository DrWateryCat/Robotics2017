'''
Created on Jan 28, 2017

@author: Kenny
'''
from robotpy_ext.common_drivers import xl_max_sonar_ez
from wpilib.smartdashboard import SmartDashboard
from networktables.networktable import NetworkTable

class Sensor:
    '''
    classdocs
    '''
    
    sonar = xl_max_sonar_ez.MaxSonarEZAnalog
    
    def __init__(self):
        self.sd = NetworkTable.getTable('SmartDashboard')
        self.sonar_multilpier = 1
        self.sonar_trim = 20
    
    def set_sonar_multiplier(self, multiplier):
        self.sonar_multilpier = multiplier
    
    def execute(self):
        SmartDashboard.putNumber("sonar_distance", self.sonar.get() * self.sonar_multilpier + self.sonar_trim)