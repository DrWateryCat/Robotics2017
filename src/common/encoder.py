'''
Created on Jan 19, 2017

@author: Kenny
'''
import ctre

class Encoder(object):
    '''
    classdocs
    '''
    
    def __init__(self, motor: ctre.CANTalon, reverse=False):
        self.motor = motor
        self.mod = 1
        if reverse:
            self.motor.reverseSensor(1)
            
        self.initial = self.mod * self.motor.getEncPosition()
        
    def get(self):
        return (self.mod * self.motor.getEncPosition()) - self.initial
    
    def zero(self):
        self.initial = self.mod * self.motor.getEncPosition()