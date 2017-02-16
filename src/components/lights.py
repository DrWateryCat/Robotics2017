from common import ledstrip
import wpilib
from wpilib.smartdashboard import SmartDashboard

class Lights:
    '''
    classdocs
    '''
    
    leds = ledstrip.LEDStrip
    
    def __init__(self, default=ledstrip.LEDStrip.Command.RED):
        '''
        Constructor
        '''
        self.command = default
        
        self.chooser = wpilib.SendableChooser()
        self.chooser.addDefault("Red", ledstrip.LEDStrip.Command.RED)
        self.chooser.addObject("Blue", ledstrip.LEDStrip.Command.BLUE)
        self.chooser.addObject("Green", ledstrip.LEDStrip.Command.GREEN)
        self.chooser.addObject("Rainbow", ledstrip.LEDStrip.Command.RAINBOW)
        self.chooser.addObject("Theater Blue", ledstrip.LEDStrip.Command.THEATER_BLUE)
        self.chooser.addObject("Theater Red", ledstrip.LEDStrip.Command.THEATER_RED)
        self.chooser.addObject("Theater Rainbow", ledstrip.LEDStrip.Command.THEATER_RAINBOW)
        
        SmartDashboard.putData("LEDs", self.chooser)



    def set_command(self, cmd):
        self.command = cmd
        
    def execute(self):
        self.leds.send_command(self.chooser.getSelected())