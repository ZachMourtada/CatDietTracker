import RPi.GPIO as GPIO
from hx711 import HX711

class LoadCellClass:
    def __init__(self, dt, sck):
        GPIO.setmode(GPIO.BCM)
        
        self.hx = HX711(dout_pin=dt, pd_sck_pin=sck)
        self.hx.zero()
    def calibrate(self):
        self.hx.zero()
        input("place known weight on scale and press enter")
        reading = self.hx.get_data_mean(readings=100)
        known_weight_g = input("enter the known weight in grams and press enter: ")

        value = float(known_weight_g)
        ratio = reading / value

        self.hx.set_scale_ratio(ratio)
    def get_reading(self, p_readings):
        weight = self.hx.get_weight_mean(readings=p_readings)
        print("Weight: {:.2f} g".format(weight))
        return weight
