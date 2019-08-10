import cv2
import os
from common import *

# image_folder = './img'
# label_folder = './merge'
# dict_path = './merge/dict.txt'

image_folder = '/media/hy17003/C022AA4B225A6D42/data/hand_dataset/hand_all/images'
label_folder = '/media/hy17003/C022AA4B225A6D42/data/hand_dataset/hand_all/merge'
check_folder = '/media/hy17003/C022AA4B225A6D42/data/hand_dataset/hand_all/check'
dict_path = '/media/hy17003/C022AA4B225A6D42/data/hand_dataset/hand_all/merge/dict.txt'


class_dict = read_dict(dict_path)
image_list = os.listdir(image_folder)
print('{} images found'.format(len(image_list)))
colors = [(0, 255, 0), (0, 0, 255), (255, 0, 0), (255, 255, 0), (255, 0, 255)]
idx = 1
count = len(image_list)
forward = 1
while(idx < count):
    image_name = image_list[idx]
    print('idx = {}, file: {}'.format(idx, image_name))
    if forward:
        idx = idx + 1
    else:
        idx = idx - 1
    image_ext = image_name[-3:]
    if image_ext != 'jpg' and image_ext != 'png':
        continue
    image_base_name = image_name[:-4]
    image_path = os.path.join(image_folder, image_base_name + '.jpg')
    if not os.path.exists(image_path):
        continue
    im = cv2.imread(image_path)
    label_path = os.path.join(label_folder, image_base_name + '.txt')
    an = read_label_file(label_path, class_dict)
    if an == None:
        continue
    for label in an.labels:
        class_idx = label[0]
        min_x = label[1]
        min_y = label[2]
        max_x = label[3]
        max_y = label[4]
        class_name = an.label_dict[class_idx]
        cv2.rectangle(im, (min_x, min_y), (max_x, max_y), colors[class_idx - 1], 1)
        cv2.putText(im, class_name, (min_x, min_y - 10), 1, 2, colors[class_idx - 1], 1)
    cv2.imshow('image', im)
    key = cv2.waitKey(0)
    if key == 110: #n
        print('please check image: ', image_path)
        dst_file = os.path.join(check_folder, image_base_name + '.jpg')
        movefile(image_path, dst_file)
    elif key == 81:
        forward = 0
    else:
        forward = 1



