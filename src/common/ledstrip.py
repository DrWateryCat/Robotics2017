import wpilib

class LEDStrip(object):
    '''
    classdocs
    '''
    
    class Command:
        RED = 0x01
        GREEN = 0x02
        BLUE = 0x03
        RAINBOW = 0x04
        THEATER_RED = 0x05
        THEATER_BLUE = 0x06
        THEATER_RAINBOW = 0x07

    def __init__(self, port=wpilib.I2C.Port.kOnboard, simPort=0):
        '''
        Constructor
        '''
        self.i2c = wpilib.I2C(port, 0x4A, simPort=simPort)
        
        #Register 0x0A: command
        #Command 0x01: Red
        #Command 0x02: Green
        #Command 0x03: Blue
        #Command 0x04: Rainbow
        #Command 0x05: Theater Chase Red
        #Command 0x06: Theater Chase Blue
        #Command 0x07: Theater Chase Rainbow
        
    def send_command(self, cmd):
        self.i2c.write(0x0A, cmd)