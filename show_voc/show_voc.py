import os
import cv2

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

# annotation_dir = './sample/annotations'
# image_dir = './sample/images'

# annotation_dir = 'E:/DataSet/hand_face/annotation'
# image_dir = 'E:/DataSet/hand_face/image'

# annotation_dir = '../voc_enhance/sample/dst_annotations'
# image_dir = '../voc_enhance/sample/dst_image'

# image_dir = 'E:/DataSet/hand_face/other_image/image'
# annotation_dir = 'E:/DataSet/hand_face/other_image/hand'

annotation_dir = 'E:/DataSet/VOCdevkit/VOC2007/Annotations'
image_dir = 'E:/DataSet/VOCdevkit/VOC2007/JPEGImages'

color_table = [(0, 0, 255), (0, 255, 255), (0, 255, 0), (255, 0, 0), (255, 0, 255), (255, 255, 0), (255, 255, 255)]
color_dict = {}
idx = 0
def GetAnnotBoxLoc(AnotPath):
    Context = {}
    tree = ET.ElementTree(file=AnotPath)
    root = tree.getroot()
    ObjectSet=root.findall('object')
    filename = root.find('filename').text
    size = root.find('size')
    width = int(size.find('width').text)
    height = int(size.find('height').text)
    print('anno -- {} height:{}, width:{}'.format(filename, height, width))
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
    print('im -- {} height:{}, width:{}, channel:{}'.format(filename, image.shape[0], image.shape[1], image.shape[2]))
    for key, boxes in info['objects'].items():
        if key not in color_dict.keys():
            idx = idx + 1
            idx = idx % len(color_table)
            color_dict[key] = color_table[idx]
        count = len(boxes)
        for box in boxes:
            p1 = (box[0], box[1])
            p2 = (box[2], box[3])
            p3 = (box[0] + 5, box[1] + 15)
            cv2.rectangle(image, p1, p2, color_dict[key], 1)
            cv2.putText(image, key, p3, cv2.FONT_HERSHEY_COMPLEX, 1.0, color_dict[key], 1)
    cv2.imshow('image', image)
    key = cv2.waitKey(0)
    if key == 27:
        break


print("finish!")
