from classes import CameraClass
from classes import EmailerClass
from classes import ModelClass
from classes import MotionSensorClass
from classes import LoadCellClass
from PIL import Image
import os
import time
email_bot = EmailerClass(param_sender="pimessenger.80@gmail.com", param_password="zttq kvuk hmnj qmzu")
camera_bot = CameraClass()
model_bot = ModelClass(param_onnx_weights_path="model_/cat_model_v3.onnx", param_categories_list_json="model_/categories.json")
motion_sensor_bot = MotionSensorClass()
load_cell_bot = LoadCellClass(dt=6, sck=5)

def cycle():
    cat_is_gone = False
    while not cat_is_gone:
        
        if (motion_sensor_bot.detect_motion_f1(1)):
            new_photo_path, date_time = camera_bot.take_photo(root_img_path="../cats/photos/unprocessed")
            class_index, class_label = model_bot.run_interface(new_photo_path)
            if class_label != "nothing":
                os.rename(new_photo_path, f"../cats/photos/{class_label}/{class_label}_{date_time}.jpg")
                time.sleep(5)

            else: cat_is_gone = True
    return


def main():
    try:
        receiver = "jaketdev@gmail.com"
        print("Calibrating load cell...")
        load_cell_bot.calibrate()
        load_cell_bot.get_reading(p_readings=100)
        print("Done")
        try:
            while True:
                if (motion_sensor_bot.detect_motion_f1(1)):
                    
                    new_photo_path, date_time = camera_bot.take_photo(root_img_path="../cats/photos/unprocessed/unprocessed.")
                    
                    class_index, class_label = model_bot.run_interface(new_photo_path)
                    
                    if class_label != "nothing":
                        os.rename(new_photo_path, f"../cats/photos/{class_label}/{class_label}_{date_time}.jpg")
                        init_weight = load_cell_bot.get_reading(p_readings=100)
                        cycle()
                        
                        final_weight = load_cell_bot.get_reading(p_readings=100)
                        food_eaten = init_weight - final_weight
                        subject = f"{class_label} seen {date_time}"
                        body = f"""
                        {class_label} visited the food bowl on {date_time}
                        They ate {food_eaten} g of food
                                """
                        print(body)
                        
                        msg = email_bot.make_msg(subject=subject, body=body, file_path=new_photo_path)
                        email_bot.mail_msg(receiver, msg)
                        with open("../cats/data.txt", "a", encoding="utf-8") as f:
                            f.write(f"{date_time} {class_label}\n")
                            f.write(f"Food eaten: {food_eaten} g\n")
                    else:
                        print("nothing!!!")
                        if os.path.exists(new_photo_path):
                            os.remove(new_photo_path)
                    time.sleep(60)

                        
                    if time.strftime("%A:%H:%M:%S") == "Sunday:00:00:00":
                        msg = email_bot.make_msg(subject="Weekly Report", body="Weekly Report", file_path="../cats/data.txt")
                        email_bot.mail_msg(receiver, msg)
                        
        except KeyboardInterrupt:
            print("Canceled")
                
    except KeyboardInterrupt:
        print(": Canceled")
    

if __name__ == "__main__":
    main()