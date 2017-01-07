'''
Created on Oct 28, 2016

@author: Kenny
'''
class UnifiedJoystick(object):
    '''
    A class to allow for unified output of buttons from 2+ joysticks
    '''
    
    def __init__(self, *args, **kwargs):
        """
        Keyword args:
        
        leftJoystick
        rightJoystick
        
        Positional args:
        leftJoystick, rightJoystick
        
        TODO: Add more than 2 joysticks, if that would ever come up
        """
        
        #Keyword args
        self.leftJoystick = kwargs.pop('leftJoystick', None)
        self.rightJoystick = kwargs.pop('rightJoystick', None)
        
        #Posititional args
        if len(args) == 2:
            self.leftJoystick = args[0]
            self.rightJoystick = args[1]
        else:
            raise ValueError("Either not enough inputs, or too many, try only using 2")
        
    def getButton(self, button):
        """
        Calls getRawButton, then or's the output
        """
        
        return (self.leftJoystick.getRawButton(button) or self.rightJoystick.getRawButton(button))