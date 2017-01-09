'''
Created on Jan 7, 2017

@author: Kenny
'''
import requests
from common.contour import Contour
from configparser import ConfigParser

class Vision:
    '''
    classdocs
    '''
    
    DRIVER_STATION_IP = "10.21.86.10:5801"
    REST_PATH = "/GRIP/data/contours/"
    
    CAMERA_FOV = 68.5
    CAMERA_WIDTH = 320
    CAMERA_HEIGHT = 240
    
    def __init__(self):
        self.detects_hook = False
        self.number_of_targets = 0
        self.hook_positionX = 0
        self.hook_positionY = 0
        
        self.read_config()
        
    def read_config(self):
        config = ConfigParser()
        config.read('visionconfig.cfg')
        if 'hostname' in config and 'port' in config:
            self.DRIVER_STATION_IP = config['hostname'] + ':' + config['port']
        else:
            self.DRIVER_STATION_IP = "10.21.86.10:5801"
        
    def get_contours_from_json(self, json):
        contours = []
        for i in self.number_of_targets:
            area = json['area'][i]
            centerX = json['centerX'][i]
            centerY = json['centerY'][i]
            width = json['width'][i]
            height = json['height'][i]
            contours.append(Contour(area=area, centerX=centerX, centerY=centerY, width=width, height=height))
        return contours
    
    def convert_to_aiming_system(self, pointX, pointY):
        retX = (pointX - (self.CAMERA_WIDTH / 2)) / (self.CAMERA_WIDTH / 2)
        retY = (pointY - (self.CAMERA_HEIGHT / 2)) / (self.CAMERA_HEIGHT / 2)
        
        return retX, retY
    
    def find_hook(self, contours):
        if self.number_of_targets < 2:
            self.detects_hook = False
            self.hook_positionX = 0
            self.hook_positionY = 0
            return
        else:
            #Hook should be between those 2 vision targets
            self.detects_hook = True
            left_target = contours[0]
            right_target = contours[1]
            
            center_x = (left_target.centerX + right_target.centerX) / 2
            center_y = (left_target.centerY + right_target.centerY) / 2
            
            hookX, hookY = self.convert_to_aiming_system(center_x, center_y)
            
            self.hook_positionX = hookX
            self.hook_positionY = hookY
    
    def execute(self):
        r = requests.get(self.DRIVER_STATION_IP + self.REST_PATH)
        targets = r.json()['contours']
        self.number_of_targets = len(targets['area'])
        contours = self.get_contours_from_json(targets)
        self.find_hook(contours)