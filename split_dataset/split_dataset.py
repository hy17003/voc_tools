from file_operator import *
import os
import random

src_img_dir = '/home/hy17003/data/upper_body/images'
src_ann_dir = '/home/hy17003/data/upper_body/annotations'
train_img_dir = '/home/hy17003/data/upper_body/train'
train_ann_dir = '/home/hy17003/data/upper_body/train'
test_img_dir = '/home/hy17003/data/upper_body/test'
test_ann_dir = '/home/hy17003/data/upper_body/test'

split_rate = 0.8


img_list = os.listdir(src_img_dir)
random.shuffle(img_list)
count = len(img_list)
train_count = int(count * split_rate)
for idx in range(count):
    base_name = img_list[idx].split('.')[0]
    img_path = os.path.join(src_img_dir, img_list[idx])
    ann_path = os.path.join(src_ann_dir, base_name + '.xml')
    if idx < train_count:
        dst_img_path = os.path.join(train_img_dir, img_list[idx])
        dst_ann_path = os.path.join(train_ann_dir, base_name + '.xml')
    else:
        dst_img_path = os.path.join(test_img_dir, img_list[idx])
        dst_ann_path = os.path.join(test_ann_dir, base_name + '.xml')
    copy_file(img_path, dst_img_path)
    copy_file(ann_path, dst_ann_path)

print('finish!')

