from gpiozero import DigitalInputDevice

import RPi.GPIO as GPIO

from datetime import datetime

import time
class MotionSensorClass:
    def __init__(self):
        self.pir_sensor = 23

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pir_sensor, GPIO.IN)

    def detect_motion_f1(self, delay_seconds):
        
        try: 
            while True:

                print(GPIO.input(self.pir_sensor))
                time.sleep(delay_seconds)
                if (GPIO.input(self.pir_sensor) == 1):
                    print(GPIO.input(self.pir_sensor))
                    return True


        except KeyboardInterrupt:
            print(" end")