# Rplidar program for communicating with UV LEDs
# This code sends power to the power relay on the appropriate GPIO pins for turning on the UV LEDs
# Last update 3/25/2022 - Edgar Macias

import os
import sys
import time
import RPi.GPIO as GPIO
import adafruit_rplidar as raslidar
from math import cos, sin, pi, floor
import numpy as np

#Setup LEDs
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)

# Setup the RPLidar
PORT_NAME = '/dev/ttyUSB0'
lidar = raslidar.RPLidar(None, PORT_NAME, timeout=3)

lidar.stop_motor()
lidar.stop()
lidar.disconnect()
lidar = raslidar.RPLidar(None, PORT_NAME, timeout=3)

# Setup the data info for 360 degrees around the core of the Lidar
scan_data = [0] * 360

num_points = 60

def processData(scanData):
    # scan_points = np.asarray(np.array_split(scan_points, num_points))
    # scan_points = [item[0] for item in scan_points]
    print(scanData)

# Continuously runs at all times, unless keyboard interrupts the program
try:
    # print(lidar.get_info())
    for scan in lidar.iter_scans():
        for (_, angle, distance) in scan:
            scan_data[int(min([359, angle]))] = distance
        processData(scan_data)
    
    
        
    #     # Filters the data to be read between angles 219 and 360 from the core of the Lidar 
    #     if angle > 219 and angle < 360 and angle != 0:
    #         # Distance is in mm
    #         # This if statement is important to control the UV LEDs
    #         # When the Lidar detects an object further than the length of the arm (508 mm) the program will turn off the UV LEDs
    #         if distance > 508 and distance != 0:
    #             # Simulates turning off the UV LEDs
    #             GPIO.output(18,GPIO.LOW)
    #             print('off')
    #         # When the Lidar detects an object within the length of the arm, the program will turn on the UV LEDs
    #         if distance <= 508 and distance != 0:
    #             # Simulates turning on the UV LEDs
    #             GPIO.output(18,GPIO.HIGH)
    #             print('off')
    #       else:
    #           pass
# Is included to safely turn off the Lidar system
        
except KeyboardInterrupt:
    print('Stopping.')
    lidar.stop_motor()
    lidar.stop()
    lidar.disconnect()
    
    # return data
