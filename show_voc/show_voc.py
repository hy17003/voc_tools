import os
import cv2

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

annotation_dir = '/home/hy17003/data/upper_body/annotations'
image_dir = '/home/hy17003/data/upper_body/images'

def GetAnnotBoxLoc(AnotPath):
    Context = {}
    tree = ET.ElementTree(file=AnotPath)
    root = tree.getroot()
    ObjectSet=root.findall('object')
    filename = root.find('filename').text
    Context['image_name'] = filename
    Objects = {}
    for Object in ObjectSet:
        ObjName=Object.find('name').text
        BndBox=Object.find('bndbox')
        x1 = int(BndBox.find('xmin').text)
        y1 = int(BndBox.find('ymin').text)
        x2 = int(BndBox.find('xmax').text)
        y2 = int(BndBox.find('ymax').text)
        BndBoxLoc=[x1,y1,x2,y2]
        if ObjName in Objects:
            Objects[ObjName].append(BndBoxLoc)
        else:
            Objects[ObjName]=[BndBoxLoc]
    Context['objects'] = Objects
    return Context



annotation_list = os.listdir(annotation_dir)
for anntation_file in annotation_list:
    anntation_path = os.path.join(annotation_dir, anntation_file)
    info = GetAnnotBoxLoc(anntation_path)
    filename = info['image_name']
    image_path = os.path.join(image_dir, filename)
    image = cv2.imread(image_path)
    for key, boxes in info['objects'].items():
        count = len(boxes)
        for box in boxes:
            p1 = (box[0], box[1])
            p2 = (box[2], box[3])
            p3 = (box[0] + 5, box[1] + 15)
            cv2.rectangle(image, p1, p2, (0, 255, 0), 2)
            cv2.putText(image, key, p3, cv2.FONT_HERSHEY_COMPLEX, 1.0, (0, 0, 255), 2)
    cv2.imshow('image', image)
    key = cv2.waitKey(0)
    if key == 27:
        break


print("finish!")
