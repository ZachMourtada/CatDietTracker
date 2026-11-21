from picamera2 import Picamera2, Preview
from picamera2.encoders import H264Encoder
import time
class CameraClass:
    def __init__(self):
        self.cam = Picamera2()
        self.cam_config_preview = self.cam.create_preview_configuration()
    
    def take_manual_photo(self, root_img_path):
        date_time = time.ctime(time.time())
        path = root_img_path + "." + date_time + ".jpg"
        self.cam.configure(self.cam_config_preview)
        self.cam.start_preview(Preview.QTGL)
        self.cam.start()
        input("capture? (return/entr): ")
        self.cam.capture_file(path)
        return path, date_time
    
    def take_photo(self, root_img_path, delay_seconds=0, num_photos=1, show_preview = False):
        self.cam.configure(self.cam_config_preview)
        if show_preview:
            self.cam.start_preview(Preview.QTGL)
        date_time = time.strftime("%m.%d.%H:%M:%S")
        self.cam.start()
        for i in range(num_photos):
            
            path = root_img_path + str(i) + "." + date_time + ".jpg"
            time.sleep(delay_seconds)
            self.cam.capture_file(path)
        self.cam.stop()
        return path, date_time


#CameraClass().take_manual_photo("/home/pi/Desktop/test")
