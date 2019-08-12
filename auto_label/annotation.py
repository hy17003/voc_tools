import os
from skimage import io
import os

try:
    import xml.etree.cElementTree as ET #解析xml的c语言版的模块
except ImportError:
    import xml.etree.ElementTree as ET

class Object:
    def __init__(self):
        self.name = ''
        self.minX = 0
        self.minY = 0
        self.maxX = 0
        self.maxY = 0

class Annotation:
    def __init__(self):
        self.filename = ''
        self.width = 0
        self.height = 0
        self.depth = 0
        self.objs = []

    def read_from_txt(self, filepath, classmap):
        if os.path.isfile(filepath):
            self.filename = os.path.basename(filepath).split(".")[0] + ".jpg"
            with open(filepath, 'r') as file:
                file_info = file.readline().split(' ')
                self.height = int(file_info[0])
                self.width = int(file_info[1])
                self.depth = int(file_info[2])
                while(True):
                    obj_info = file.readline().split(' ')
                    if not obj_info or len(obj_info) != 5:
                        break
                    obj = Object()
                    class_idx = int(obj_info[0])
                    obj.name = classmap[class_idx]
                    obj.minX = int(obj_info[1])
                    obj.minY = int(obj_info[2])
                    obj.maxX = int(obj_info[3])
                    obj.maxY = int(obj_info[4])
                    self.objs.append(obj)

    def write_to_xml(self, filepath):
        with open(filepath, 'w') as annotation:
            annotation.write('<?xml version="1.0" ?>\n')
            annotation.write("<annotation>\n")
            #folder
            annotation.write("<folder>")
            annotation.write("VOC2007")
            annotation.write("</folder>\n")
            #filename
            annotation.write("<filename>")
            annotation.write(self.filename)
            annotation.write("</filename>\n")
            #source
            annotation.write("<source>\n")
            annotation.write("  <database>")
            annotation.write("Unknown")
            annotation.write("</database>\n")
            annotation.write("</source>\n")
            #size
            annotation.write("<size>\n")
            annotation.write("  <width>")
            annotation.write(str(self.width))
            annotation.write("</width>\n")

            annotation.write("  <height>")
            annotation.write(str(self.height))
            annotation.write("</height>\n")

            annotation.write("  <depth>")
            annotation.write(str(self.depth))
            annotation.write("</depth>\n")
            annotation.write("</size>\n")
            #segmented
            annotation.write("<segmented>")
            annotation.write(str(0))
            annotation.write("</segmented>\n")
            #object
            for i in range(len(self.objs)):
                annotation.write("<object>")
                annotation.write("  <name>")
                annotation.write(self.objs[i].name)
                annotation.write("</name>\n")

                annotation.write("  <pose>")
                annotation.write("Unspecified")
                annotation.write("</pose>\n")

                annotation.write("  <truncated>")
                annotation.write(str(0))
                annotation.write("</truncated>\n")

                annotation.write("  <difficult>")
                annotation.write(str(0))
                annotation.write("</difficult>\n")

                annotation.write("  <bndbox>\n")
                annotation.write("    <xmin>")
                annotation.write(str(self.objs[i].minX))
                annotation.write("</xmin>\n")

                annotation.write("    <ymin>")
                annotation.write(str(self.objs[i].minY))
                annotation.write("</ymin>\n")

                annotation.write("    <xmax>")
                annotation.write(str(self.objs[i].maxX))
                annotation.write("</xmax>\n")

                annotation.write("    <ymax>")
                annotation.write(str(self.objs[i].maxY))
                annotation.write("</ymax>\n")
                annotation.write("  </bndbox>\n")
                annotation.write("</object>\n")
            annotation.write("</annotation>")

    def read_from_xml(self, file_path):#AnotPath VOC标注文件路径 #
        tree = ET.ElementTree(file=file_path) #打开文件，解析成一棵树型结构
        root = tree.getroot()#获取树型结构的根
        self.filename = root.find('filename').text
        size = root.find('size')
        if size is None:
            return False
        self.width = int(size.find('width').text)
        self.height = int(size.find('height').text)
        self.depth = int(size.find('depth').text)
        ObjectSet=root.findall('object')#找到文件中所有含有object关键字的地方，这些地方含有标注目标
        for obj in ObjectSet:
            ObjName=obj.find('name').text
            BndBox=obj.find('bndbox')
            x1 = int(BndBox.find('xmin').text)#-1 #-1是因为程序是按0作为起始位置的
            y1 = int(BndBox.find('ymin').text)#-1
            x2 = int(BndBox.find('xmax').text)#-1
            y2 = int(BndBox.find('ymax').text)#-1

            x1 = max(x1, 0)
            y1 = max(y1, 0)
            x2 = min(x2, self.width - 1)
            y2 = max(y2, self.height - 1)

            if (x2 - x1) * (y2 - y1) < 900:
                continue

            new_obj = Object()
            new_obj.name = ObjName
            new_obj.minX = x1
            new_obj.minY = y1
            new_obj.maxX = x2
            new_obj.maxY = y2
            self.objs.append(new_obj)
        return True

