import os
from common import *

'''
两个文件夹，每个文件夹中应包括标注文件，标注文件名与对应的图像名相同，内容格式如下：
image_height image_width image_channel
class_idx min_x min_y max_x max_y
	.
	.
	.
文件夹中还应包括一个dict.txt文件，内容格式如下：
class_idx class_name
	.
	.
	.
其中class_idx从1开始，依次递增
'''

folder1 = './c1'
dict1 = './c1/dict.txt'

folder2 = './c2'
dict2 = './c2/dict.txt'

merge_folder = './merge'

c1_list = os.listdir(folder1)
c2_list = os.listdir(folder2)

anntoation_sets = []
dict1 = read_dict(os.path.join(folder1, 'dict.txt'))
dict2 = read_dict(os.path.join(folder2, 'dict.txt'))
new_dict = merge_dict(dict1, dict2)
for file1 in c1_list:
    if file1 == 'dict.txt':
        continue
    file1_path = os.path.join(folder1, file1)
    an1 = read_label_file(file1_path, dict1)
    bfind = 0
    for file2 in c2_list:
        if file1 == file2:
            c2_list.remove(file2)
            bfind = 1
            break
    if bfind:
        file2_path = os.path.join(folder2, file2)
        an2 = read_label_file(file2_path, dict2)
        an_m = merge_annotation(an1, an2)
        if an_m != None:
            anntoation_sets.append(an_m)
    else:
        an1 = update_dict(an1, new_dict)
        anntoation_sets.append(an1)

for file2 in c2_list:
    if file2 == 'dict.txt':
        continue
    file2_path = os.path.join(folder2, file2)
    an2 = read_label_file(file2_path, dict2)
    an2 = update_dict(an2, new_dict)
    anntoation_sets.append(an2)

#save anntoation_sets
new_dict_path = os.path.join(merge_folder, 'dict.txt')
with open(new_dict_path, 'w') as f:
    for key, val in anntoation_sets[0].label_dict.items():
        line = '{} {}\n'.format(key, val)
        f.writelines(line)

for an in anntoation_sets:
    file_name = an.file_name
    file_path = os.path.join(merge_folder, file_name)
    with open(file_path, 'w') as f:
        image_info = '{} {} {}\n'.format(an.height, an.width, an.channel)
        f.writelines(image_info)
        for label in an.labels:
            label_info = '{} {} {} {} {}\n'.format(label[0], label[1], label[2], label[3], label[4])
            f.writelines(label_info)
print('merge finish!')






