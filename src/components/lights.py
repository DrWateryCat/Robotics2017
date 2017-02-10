from common import ledstrip

class Lights:
    '''
    classdocs
    '''
    
    leds = ledstrip.LEDStrip
    
    def __init__(self, default=ledstrip.LEDStrip.Command.RAINBOW):
        '''
        Constructor
        '''
        self.command = default
    
    def set_command(self, cmd: ledstrip.LEDStrip.Command):
        self.command = cmd
        
    def execute(self):
        self.leds.send_command(self.command)