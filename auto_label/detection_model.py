import cv2
import numpy as np
from cv2 import dnn

class Target:

    def __init__(self):
        self.class_name = None
        self.box = None
        self.conf = 0


class SSDModel:

    def __init__(self):
        self.net = None
        self.dict = None
        self.width = 0
        self.height = 0
        self.scale = 1.0
        self.mean_val = 0.0
        self.threshold = 0.6

    def load_model(self, modelTxt, modelBin, classDict, width=300, height = 300, scale = 0.00783, meanVal = 127.5):
        self.net = dnn.readNetFromCaffe(modelTxt, modelBin)
        self.dict = classDict
        self.width = width
        self.height = height
        self.scale = scale
        self.mean_val = meanVal


    def detect(self, image):
        result = []
        (h, w, c) = image.shape
        blob = dnn.blobFromImage(cv2.resize(image, (self.width, self.height)), self.scale,
                                 (self.width, self.height), self.mean_val)
        self.net.setInput(blob)
        detections = self.net.forward()
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > self.threshold:
                idx = int(detections[0, 0, i, 1])
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                box = box.astype("int")
                obj = Target()
                obj.class_name = self.dict[idx]
                obj.box = box
                obj.conf = confidence
                result.append(obj)
        return result



