from voc_enhance.Annotation import *
import os, shutil


# xml_folder = 'E:/DataSet/hand_face/other_image/bak'
# dst_folder = 'E:/DataSet/hand_face/other_image/Annotations'
# xml_list = os.listdir(xml_folder)
# for xml_file in xml_list:
#     pos = xml_file.find('_', 0)
#     #pos = xml_file.find('_', pos + 1)
#     #pos = xml_file.find('_', pos + 1)
#     dst_file = xml_file[pos + 1:]
#     an = Annotation()
#     src_an_path = os.path.join(xml_folder, xml_file)
#     an.read_from_xml(src_an_path)
#     dst_an_path = os.path.join(dst_folder, dst_file)
#     an.write_to_xml(dst_an_path)


img_folder = 'E:/DataSet/hand_face/other_image/image'
src_folder = 'E:/DataSet/WiderFace/Annotations_bak'
dst_folder = 'E:/DataSet/hand_face/other_image/labels'

def movefile(srcfile,dstfile):
    if not os.path.isfile(srcfile):
        print("%s not exist!"%(srcfile))
    else:
        fpath,fname=os.path.split(dstfile)    #分离文件名和路径
        if not os.path.exists(fpath):
            os.makedirs(fpath)                #创建路径
        shutil.move(srcfile,dstfile)          #移动文件
        print("move %s -> %s"%( srcfile,dstfile))

def copyfile(srcfile,dstfile):
    if not os.path.isfile(srcfile):
        print("%s not exist!"%(srcfile))
    else:
        fpath,fname=os.path.split(dstfile)    #分离文件名和路径
        if not os.path.exists(fpath):
            os.makedirs(fpath)                #创建路径
        shutil.copyfile(srcfile,dstfile)      #复制文件
        print("copy %s -> %s"%( srcfile,dstfile))

img_list = os.listdir(img_folder)
for img_file in img_list:
    img_base_name = img_file.split('.')[0]
    src_xml_file = os.path.join(src_folder, img_base_name + '.xml')
    dst_xml_file = os.path.join(dst_folder, img_base_name + '.xml')
    copyfile(src_xml_file, dst_xml_file)