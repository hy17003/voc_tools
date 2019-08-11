import os
import cv2
#from Annotation import *
from voc_enhance.Annotation import *

input_image_folder = './sample/src_image'
input_annotation_foler = './sample/src_annotations'
output_image_folder = './sample/dst_image'
output_annotation_foler = './sample/dst_annotations'


def flip(input_annotation, input_image):
    output_annotation = Annotation()
    output_annotation.filename = input_annotation.filename.split('.')[0] + '_flip.jpg'
    output_annotation.width = input_annotation.width
    output_annotation.height = input_annotation.height
    output_annotation.depth = input_annotation.depth
    for src_obj in input_annotation.objs:
        dst_obj = Object()
        dst_obj.name = src_obj.name
        dst_obj.minY = src_obj.minY
        dst_obj.maxY = src_obj.maxY
        dst_obj.minX = output_annotation.width - src_obj.maxX
        dst_obj.maxX = output_annotation.width - src_obj.minX
        output_annotation.objs.append(dst_obj)
    output_image = cv2.flip(input_image, 1)
    return output_annotation, output_image


src_annotation_list = os.listdir(input_annotation_foler)
for annotation_file in src_annotation_list:
    an = Annotation()
    src_annotation_path = os.path.join(input_annotation_foler, annotation_file)
    an.read_from_xml(src_annotation_path)
    print('process ', an.filename)
    src_image_path = os.path.join(input_image_folder, an.filename)
    im = cv2.imread(src_image_path)
    if im is None:
        continue
    new_an, new_image = flip(an, im)
    base_name = new_an.filename.split('.')[0]
    dst_annotation_path = os.path.join(output_annotation_foler, base_name + '.xml')
    dst_image_path = os.path.join(output_image_folder, base_name + '.jpg')
    new_an.write_to_xml(dst_annotation_path)
    cv2.imwrite(dst_image_path, new_image)






