import os
import skimage.io as io
from Annotation import *

'''
程序的目的是读取voc格式的标注文件，对其超出图像范围的
标注进行纠正，保存到指定目录
'''

in_anno_dir = 'E:/DataSet/VOCdevkit/VOC2007/Annotations_bak'
in_img_dir = 'E:/DataSet/VOCdevkit/VOC2007/JPEGImages'
out_anno_dir = 'E:/DataSet/VOCdevkit/VOC2007/Annotations'
#out_img_dir = 'E:/DataSet/hand_face/image'


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
    anno.height = img.shape[0]
    anno.width = img.shape[1]
    anno.depth = img.shape[2]
    anno.check()
    #out_img_path = os.path.join(out_img_dir, img_name)
    #io.imsave(out_img_path, img)
    out_anno_path = os.path.join(out_anno_dir, annotation_file)
    anno.write_to_xml(out_anno_path)
print('finish!')


