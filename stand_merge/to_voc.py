import os, sys
import numpy as np

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
        self.classmap = ['background', 'face', 'hand']

    def read(self, filepath):
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
                    obj.name = self.classmap[class_idx]
                    obj.minX = int(obj_info[1])
                    obj.minY = int(obj_info[2])
                    obj.maxX = int(obj_info[3])
                    obj.maxY = int(obj_info[4])
                    self.objs.append(obj)


root_dir = '/media/hy17003/C022AA4B225A6D42/data/hand_dataset/hand_all/hand_face_dataset/VOCdevkit/VOC2007'
annotations_dir = root_dir + '/Annotations'
imagesets_dir = root_dir + '/ImageSets'
jpegimages_dir = root_dir + '/JPEGImages'
src_dir = root_dir + '/SRC_LABEL'
dct = ['hand']

label_list = os.listdir(src_dir)
file_count = 0
for i in range(0, len(label_list)):
    path = os.path.join(src_dir, label_list[i])
    if os.path.isfile(path):
        #read label
        ano = Annotation()
        ano.read(filepath = path)
        image_name = label_list[i].split(".")[0]
        annotaiton_name = annotations_dir + "/" + image_name + ".xml"
        with open(annotaiton_name, 'w') as annotation:
            annotation.write("<annotation>\n")
            #folder
            annotation.write("<folder>")
            annotation.write("VOC2007")
            annotation.write("</folder>\n")
            #filename
            annotation.write("<filename>")
            annotation.write(ano.filename)
            annotation.write("</filename>\n")
            #source
            annotation.write("<source>\n")
            annotation.write("<database>")
            annotation.write("Unknown")
            annotation.write("</database>\n")
            annotation.write("</source>\n")
            #size
            annotation.write("<size>\n")
            annotation.write("<width>")
            annotation.write(str(ano.width))
            annotation.write("</width>\n")

            annotation.write("<height>")
            annotation.write(str(ano.height))
            annotation.write("</height>\n")

            annotation.write("<depth>")
            annotation.write(str(ano.depth))
            annotation.write("</depth>\n")
            annotation.write("</size>\n")
            #segmented
            annotation.write("<segmented>")
            annotation.write(str(0))
            annotation.write("</segmented>\n")
            #object
            for i in range(len(ano.objs)):
                annotation.write("<object>")
                annotation.write("<name>")
                annotation.write(ano.objs[i].name)
                annotation.write("</name>\n")

                annotation.write("<pose>")
                annotation.write("Unspecified")
                annotation.write("</pose>\n")

                annotation.write("<truncated>")
                annotation.write(str(0))
                annotation.write("</truncated>\n")

                annotation.write("<difficult>")
                annotation.write(str(0))
                annotation.write("</difficult>\n")

                annotation.write("<bndbox>\n")
                annotation.write("<xmin>")
                annotation.write(str(ano.objs[i].minX))
                annotation.write("</xmin>\n")

                annotation.write("<ymin>")
                annotation.write(str(ano.objs[i].minY))
                annotation.write("</ymin>\n")

                annotation.write("<xmax>")
                annotation.write(str(ano.objs[i].maxX))
                annotation.write("</xmax>\n")

                annotation.write("<ymax>")
                annotation.write(str(ano.objs[i].maxY))
                annotation.write("</ymax>\n")
                annotation.write("</bndbox>\n")
                annotation.write("</object>\n")
            annotation.write("</annotation>")
            print(file_count, "file finish!")
            file_count = file_count + 1