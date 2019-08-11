from Annotation import *
import os

# input_anno_dir1 = './sample/annotation1'
# input_anno_dir2 = './sample/annotation2'
# output_anno_dir = './sample/annotation_merge'

input_anno_dir1 = 'E:/DataSet/hand_face/other_image/face'
input_anno_dir2 = 'E:/DataSet/hand_face/other_image/hand'
output_anno_dir = 'E:/DataSet/hand_face/other_image/annotaion'

anno_list1 = os.listdir(input_anno_dir1)
anno_list2 = os.listdir(input_anno_dir2)

def merge_voc(an1, an2):
    an = Annotation()
    if an1.width != an2.width or an1.height != an2.height or an1.depth != an2.depth or an1.filename != an2.filename:
        return None
    an.filename = an1.filename
    an.width = an1.width
    an.height = an1.height
    an.depth = an1.depth
    an.objs = an1.objs + an2.objs
    return an

anno_set = []
for anno_file1 in anno_list1:
    an1 = Annotation()
    an1.read_from_xml(os.path.join(input_anno_dir1, anno_file1))
    bfind = 0
    for anno_file2 in anno_list2:
        if anno_file1 == anno_file2:
            anno_list2.remove(anno_file2)
            bfind = 1
            break
    if bfind:
        an2 = Annotation()
        an2.read_from_xml(os.path.join(input_anno_dir2, anno_file2))
        an = merge_voc(an1, an2)
        anno_set.append(an)
    else:
        anno_set.append(an1)

for anno_file2 in anno_list2:
    an2 = Annotation()
    an2.read_from_xml(os.path.join(input_anno_dir2, anno_file2))
    anno_set.append(an2)

for anno in anno_set:
    filename = os.path.join(output_anno_dir, anno.filename.split('.')[0] + '.xml')
    anno.write_to_xml(filename)


