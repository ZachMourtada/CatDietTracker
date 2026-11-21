import onnxruntime
import numpy as np
import json
import time
from PIL import Image

class ModelClass:
    
    def __init__(self, param_onnx_weights_path, param_categories_list_json):
        super()
        self._onnx_weights_path = param_onnx_weights_path
        self._categories_list_json = param_categories_list_json
        self._ort_session = onnxruntime.InferenceSession(self._onnx_weights_path, providers=['CPUExecutionProvider'])
        self._MEAN = [0.485, 0.456, 0.406]
        self._STD = [0.229, 0.224, 0.225]
        
        with open(self._categories_list_json, "r") as file:
            self._img_net_classes = json.load(file)
            print(type(self._img_net_classes))
        
        
    def crop_resize(self, image, new_size):
        width, height = image.size
        min_dim = min(width, height)
        
        left = (width - min_dim) // 2
        upper = (height - min_dim) // 2
        right = left + min_dim
        lower = upper + min_dim
        
        square_image = image.crop((left,upper,right,lower))
        
        resized_image = square_image.resize((new_size, new_size))
        #resized_image.show()
        return resized_image
    
    def image_normalize_reshape(self, image):
        
        h, w, c = image.shape
        image = image.transpose((2, 0, 1)) / 255.0
        print("transoped:", image)
        np_means = np.array(self._MEAN).reshape(c,1,1)
        np_stds = np.array(self._STD).reshape(c,1,1)
        print("means:", np_means)
        print("stds:", np_stds)
        
        norm_image = (image - np_means) / (np_stds + 1e-6)
        
        
        
        return np.expand_dims(norm_image, 0).astype(np.float32)
    
    def load_onnx_input(self, image_path):
        cropped_image = self.crop_resize(Image.open(image_path).convert('RGB'), 224)
        np_image = np.array(cropped_image)
        image_array = np.asarray(cropped_image, dtype = np.float32)
        print("pixel:", image_array[223,223])
        
        norm_image = self.image_normalize_reshape(np_image)
        print("shape:", norm_image.shape)
        print("dtype:", norm_image.dtype)
        print("min:", norm_image.min())
        print("max:",norm_image.max())
        print("mean:", norm_image.mean())
        print("first 10:", norm_image.flatten()[:10])

        return {self._ort_session.get_inputs()[0].name: norm_image}
    
    def run_interface(self, image_path):
        onnxruntime_input = self.load_onnx_input(image_path)
        onnxruntime_outputs = self._ort_session.run(None, onnxruntime_input)
        print("raw output:", onnxruntime_outputs[0])
        print("pred_index:", onnxruntime_outputs[0].argmax())
        for output in onnxruntime_outputs:
            class_index = np.argmax(output)
            print("Class index:", class_index)
            print(self._img_net_classes)
            print("Class Label:", self._img_net_classes.get(str(class_index)))
            return class_index, self._img_net_classes.get(str(class_index))
            
    def time_test(self, image_path, num_runs):
        inference_time = []
        onnxruntime_input = self.load_onnx_input(image_path)
        for _ in range(num_runs):
            start_time = time.time()
            
            onnx_runtime_outputs = self._ort_session.run(None, onnxruntime_input)
            
            end_time = time.time()
            
            inference_time.append(end_time - start_time)
        print("Minimum inference time %.4fs" % np.min(inference_time))
            
    
