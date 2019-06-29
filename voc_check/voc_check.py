import os
import skimage.io

from Annotation import *

in_anno_dir = '/home/hy17003/data/upper/annotations'
in_img_dir = '/home/hy17003/data/upper/images'
out_anno_dir = '/home/hy17003/data/upper_body/annotations'
out_img_dir = '/home/hy17003/data/upper_body/images'


annotaion_list = os.listdir(in_anno_dir)
index = 0
for annotation_file in annotaion_list:
    print(index, ' :', annotation_file, 'is process...')
    index = index + 1
    annotation_path = os.path.join(in_anno_dir, annotation_file)
    anno = Annotation()
    flag = anno.read_from_xml(annotation_path)
    if flag == False:
        continue
    if len(anno.objs) == 0:
        continue
    img_name = anno.filename
    img_path = os.path.join(in_img_dir, img_name)
    img = io.imread(img_path)
    out_img_path = os.path.join(out_img_dir, img_name)
    io.imsave(out_img_path, img)
    out_anno_path = os.path.join(out_anno_dir, annotation_file)
    anno.write_to_xml(out_anno_path)
print('finish!')


