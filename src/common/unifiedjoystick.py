'''
Created on Oct 28, 2016

@author: Kenny
'''
class UnifiedJoystick(object):
    '''
    A class to allow for unified output of buttons from 2+ joysticks
    '''
    
    def __init__(self, *joysticks):
        self.joysticks = joysticks
        
        
    def getButton(self, button):
        """
        Calls getRawButton, then or's the output
        """
        
        ret = False
        for i in self.joysticks:
            ret |= i.getRawButton(button)
        return ret