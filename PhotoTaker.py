from classes import CameraClass
from classes import MotionSensorClass
import time
motion_bot = MotionSensorClass()
cam_bot = CameraClass();
batch = 0
try:
    while True:
        
        if motion_bot.detect_motion_f1(delay_seconds=0.5):
            print("Motion detected")
            cam_bot.take_photo(root_img_path=f"../cats/photos/rand/batch_{batch}_",delay_seconds=0.5, num_photos=50)
            time.sleep(90)
            batch += 1
except KeyboardInterrupt:
    print(": Canceled")
    