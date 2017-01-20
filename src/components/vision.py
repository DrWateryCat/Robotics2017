'''
Created on Jan 7, 2017

@author: Kenny
'''
import requests
from common.contour import Contour
from configparser import ConfigParser
import math
import logging

class Vision:
    '''
    classdocs
    '''
    
    DRIVER_STATION_IP = "10.21.86.10:5801"
    REST_PATH = "/GRIP/data/contours/"
    
    CAMERA_FOV = 68.5
    CAMERA_WIDTH = 320
    CAMERA_HEIGHT = 240
    FOCAL_LENGTH = 297.73
    
    def __init__(self):
        self.detects_hook = False
        self.number_of_targets = 0
        self.hookX = 0
        self.hookY = 0
        self.hook_angle = 0
        
        self.read_config()
        
    def read_config(self):
        config = ConfigParser()
        config.read('visionconfig.cfg')
        if 'hostname' in config and 'port' in config:
            self.DRIVER_STATION_IP = config['hostname'] + ':' + config['port']
        else:
            self.DRIVER_STATION_IP = "10.21.86.10:5801"
            
        if 'using_custom_http_server' in config:
            if config['using_custom_http_server'] is True:
                self.REST_PATH = "/contours"
            else:
                self.REST_PATH = "/GRIP/data/contours"
        else:
            self.REST_PATH = "/GRIP/data/contours"
        
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
    
    def convert_from_aiming_system(self, pointX, pointY):
        retX = pointX * (self.CAMERA_WIDTH / 2)
        retX = retX + (self.CAMERA_WIDTH / 2)
        
        retY = pointY * (self.CAMERA_HEIGHT / 2)
        retY = retY + (self.CAMERA_HEIGHT / 2)
        
        return retX, retY
    
    def angle_to_target(self, pointX, pointY):
        centerX = (self.CAMERA_WIDTH / 2) - 0.5
        
        ret = math.degrees(math.atan((pointX - centerX) / self.FOCAL_LENGTH))
        return ret
    
    def find_hook(self, contours):
        if self.number_of_targets < 2:
            self.detects_hook = False
            self.hookX = 0
            self.hookY = 0
            self.hook_angle = 0
            return
        else:
            #Hook should be between those 2 vision targets
            self.detects_hook = True
            left_target = contours[0]
            right_target = contours[1]
            
            center_x = (left_target.centerX + right_target.centerX) / 2
            center_y = (left_target.centerY + right_target.centerY) / 2
            
            angle_to_hook = self.angle_to_target(center_x, center_y)
            
            hookX, hookY = self.convert_to_aiming_system(center_x, center_y)
            
            self.hookX = hookX
            self.hookY = hookY
            self.hook_angle = angle_to_hook
    
    def execute(self):
        try:
            r = requests.get(self.DRIVER_STATION_IP + self.REST_PATH)
            targets = r.json()['contours']
            self.number_of_targets = len(targets['area'])
            contours = self.get_contours_from_json(targets)
            self.find_hook(contours)
        except:
            logging.log("Could not reach the vision server.", msg=logging.ERROR)
            pass