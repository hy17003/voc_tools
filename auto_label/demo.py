from annotation import *
from detection_model import *
import matplotlib.pyplot as plt
import numpy as np
import cv2

#*******************************************************************
MODEL_FOLDER = 'model'
MODEL_NUM = 2
MODEL_TXT = ['hand_deploy.prototxt',
             'face_deploy.prototxt']
MODEL_BIN = ['mobilenet_iter_17000.caffemodel',
             'res10_300x300_ssd_iter_140000_fp16.caffemodel']
CLASS_DICT = [{0: 'background', 1: 'hand'},
              {0: 'background', 1: 'face'}]
IMAGE_FOLDER = 'images'
OUTPUT_FOLDER = 'output'
#********************************************************************

def imshow(mat):
    img_new = np.zeros(mat.shape)
    img_new[:, :, 0] = mat[:, :, 2]
    img_new[:, :, 1] = mat[:, :, 1]
    img_new[:, :, 2] = mat[:, :, 0]
    img_new = img_new.astype(np.uint8)
    plt.imshow(img_new)
    plt.show()

color_table = [(0, 0, 255), (0, 255, 255), (0, 255, 0), (255, 0, 0),
               (255, 0, 255), (255, 255, 0), (255, 255, 255)]
color_dict = {}
color_idx = 0
models = []

#load model
hand_model = SSDModel()
hand_model.load_model(os.path.join(MODEL_FOLDER, MODEL_TXT[0]),
                      os.path.join(MODEL_FOLDER, MODEL_BIN[0]),
                      CLASS_DICT[0],
                      300,
                      300,
                      0.00783,
                      (127.5, 127.5, 127.5)
                      )
face_model = SSDModel()
face_model.load_model(os.path.join(MODEL_FOLDER, MODEL_TXT[1]),
                      os.path.join(MODEL_FOLDER, MODEL_BIN[1]),
                      CLASS_DICT[1],
                      300,
                      300,
                      1.0,
                      (104.0, 177.0, 123.0)
                      )
models.append(hand_model)
models.append(face_model)

#predict
image_list = os.listdir(IMAGE_FOLDER)
for image_file in image_list:
    image_path = os.path.join(IMAGE_FOLDER, image_file)
    img = cv2.imread(image_path)
    img_cpy = img.copy()
    (height, width, channel) = img.shape
    an = Annotation()
    an.width = width
    an.height = height
    an.depth = channel
    an.filename = image_file
    for model in models:
        targets = model.detect(img)
        for target in targets:
            if target.class_name not in color_dict.keys():
                color_idx = color_idx % len(color_table)
                color_dict[target.class_name] = color_table[color_idx]
                color_idx = color_idx + 1
            obj = Object()
            obj.name = target.class_name
            obj.minX = target.box[0]
            obj.minY = target.box[1]
            obj.maxX = target.box[2]
            obj.maxY = target.box[3]
            an.objs.append(obj)
            cv2.rectangle(img_cpy, (target.box[0], target.box[1]), (target.box[2], target.box[3]),
                          color_dict[target.class_name], 2)
            cv2.putText(img_cpy, target.class_name, (target.box[0], target.box[1]), cv2.FONT_HERSHEY_PLAIN,
                        1.5, color_dict[target.class_name])
    if len(an.objs) > 0:
        base_name = image_file.split('.')[0]
        save_img_path = os.path.join(OUTPUT_FOLDER, 'annotations/' + base_name + '.xml')
        an.write_to_xml(save_img_path)
        save_img_path = os.path.join(OUTPUT_FOLDER, 'images/' + base_name + '.jpg')
        cv2.imwrite(save_img_path, img)
    #imshow(img)
    cv2.imshow('image', img_cpy)
    cv2.waitKey(0)

print('finish!')





