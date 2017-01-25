'''
Created on Jan 23, 2017

@author: Kenny
'''
from pyfrc.physics.drivetrains import two_motor_drivetrain, four_motor_drivetrain

class PhysicsEngine:
    '''
    classdocs
    '''
    
    #CAN 0: left talon 0 (Encoder attached)
    #CAN 1: left talon 1
    #CAN 2: right talon 0 (Encoder attached)
    #CAN 3: right talon 1


    def __init__(self, controller):
        '''
        Constructor
        '''
        self.controller = controller
        
        self.controller.add_device_gyro_channel('navxmxp_spi_4_angle')
        self.iErr = 0
        
    def update_sim(self, hal_data, now, tm_diff):
        try:
            l0_motor = hal_data['CAN'][0]['value']/1023
            l1_motor = hal_data['CAN'][1]['value']/1023
            r0_motor = hal_data['CAN'][2]['value']/1023
            r1_motor = hal_data['CAN'][3]['value']/1023
            
            fwd, rcw = two_motor_drivetrain(l0_motor, r0_motor, speed=5)
            if abs(fwd) > 0.1:
                rcw += -(0.2*tm_diff)
                
            self.controller.drive(fwd, rcw, tm_diff)
        except:
            pass