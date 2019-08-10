import os
import shutil

class Annotaion:
    def __init__(self):
        self.width = 0
        self.height = 0
        self.channel = 0
        self.label_dict = {}
        self.labels = []
        self.file_name = ''

def merge_dict(dict1, dict2):
    new_dict = dict1.copy()
    for key2 in dict2.keys():
        bfind = False
        for new_key in new_dict.keys():
            if dict2[key2] == new_dict[new_key]:
                bfind = True
                break
        if not bfind:
            new_idx = len(new_dict.keys()) + 1
            new_dict[new_idx] = dict2[key2]
    return new_dict

def look_up_key(d, value):
    for key, val in d.items():
        if val == value:
            return key
    return None

def update_dict(an, new_dict):
    for idx in range(len(an.labels)):
        label = an.labels[idx]
        obj_idx = label[0]
        obj_name = an.label_dict[obj_idx]
        new_idx = look_up_key(new_dict, obj_name)
        an.labels[idx][0] = new_idx
    return an

def merge_annotation(a1, a2):
    an_new = Annotaion()
    if a1.file_name != a2.file_name:
        print('filename wrong!')
        exit(-1)
    an_new.file_name = a1.file_name
    if a1.width != a2.width or a1.height != a2.height or a1.channel != a2.channel:
        print('image size wrong!')
        return None
    an_new.width = a1.width
    an_new.height = a1.height
    an_new.channel = a1.channel
    an_new.label_dict = merge_dict(a1.label_dict, a2.label_dict)
    for label1 in a1.labels:
        obj1_idx = label1[0]
        obj1_minx = label1[1]
        obj1_miny = label1[2]
        obj1_maxx = label1[3]
        obj1_maxy = label1[4]
        obj1_name = a1.label_dict[obj1_idx]
        new_key = look_up_key(an_new.label_dict, obj1_name)
        if new_key == None:
            print('dict wrong!')
            exit(-1)
        new_label = [new_key, obj1_minx, obj1_miny, obj1_maxx, obj1_maxy]
        an_new.labels.append(new_label)
    for label2 in a2.labels:
        obj2_idx = label2[0]
        obj2_minx = label2[1]
        obj2_miny = label2[2]
        obj2_maxx = label2[3]
        obj2_maxy = label2[4]
        obj2_name = a2.label_dict[obj2_idx]
        new_key = look_up_key(an_new.label_dict, obj2_name)
        if new_key == None:
            print('dict wrong!')
            exit(-1)
        new_label = [new_key, obj2_minx, obj2_miny, obj2_maxx, obj2_maxy]
        an_new.labels.append(new_label)
    return an_new

def read_dict(file_path):
    label_dict = {}
    with open(file_path) as f:
        line = f.readline()
        while line:
            line = line[:-1]
            idx = int(line.split(' ')[0])
            name = line.split(' ')[1]
            label_dict[idx] = name
            line = f.readline()
    return label_dict

def read_label_file(file_path, label_dict):
    an = Annotaion()
    an.label_dict = label_dict
    an.file_name = os.path.basename(file_path)
    if not os.path.exists(file_path):
        return None
    with open(file_path) as f:
        #read head
        line = f.readline()[:-1]
        an.width = int(line.split(' ')[0])
        an.height = int(line.split(' ')[1])
        an.channel = int(line.split(' ')[2])
        line = f.readline()
        while line:
            line = line[:-1]
            label_idx = int(line.split(' ')[0])
            min_x = int(line.split(' ')[1])
            min_y = int(line.split(' ')[2])
            max_x = int(line.split(' ')[3])
            max_y = int(line.split(' ')[4])
            an.labels.append([label_idx, min_x, min_y, max_x, max_y])
            line = f.readline()
    return an


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