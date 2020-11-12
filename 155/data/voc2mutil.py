import os
import shutil
import subprocess
from threading import Thread
import xml.etree.ElementTree as ET

import cv2
import random

# 原始数据路径
orgin_img_path = 'F:/VOCdevkit/VOC2012/JPEGImages/'
# val_img_path = ''
orgin_label_path = 'F:/VOCdevkit/VOC2012/Annotations/'
# val_label_path = ''

# 提取后的路径
save_img_path = 'F:/2cls_voc/images/'
save_label_path = 'F:/2cls_voc/labels/'

divide_img_path = 'F:/mutil_voc/images/'
divide_label_path = 'F:/mutil_voc/labels/'

model = ['train', 'val']

# class_name = ['tvmonitor']
# class_plus = {0: 'train', 1: 'person', 2: 'bicycle', 3: 'car', 4: 'motorbike', 5: 'bus', 8: 'cat', 9: 'bird', 10: 'dog',
#               11: 'sheep', 21: 'bottle', 25: 'chair', 27: 'pottedplant', 33: 'tvmonitor'}
#
#
# def get_keys(d, value):
#     return [k for k, v in d.items() if v == value]
#
#
# def convert(size, box):
#     x = (box[0] + box[2]) / (2.0 * size[0])
#     y = (box[1] + box[3]) / (2.0 * size[1])
#     w = (box[2] - box[0]) / (size[0])
#     h = (box[3] - box[1]) / (size[1])
#     return ("%.6f" % x, "%.6f" % y, "%.6f" % w, "%.6f" % h)
#
#
# for xml_file in os.listdir(orgin_label_path):
#     in_file = open(os.path.join(orgin_label_path, xml_file))
#     tree = ET.parse(in_file)
#     root = tree.getroot()
#     size = root.find('size')
#     w = int(size.find('width').text)
#     h = int(size.find('height').text)
#     img_name = str(xml_file).split('.')[0]
#     with open('{}.txt'.format(os.path.join(save_label_path, img_name)), 'w') as label_file:
#         all_cls = [obj.find('name').text for obj in root.iter('object')]
#         for cls_n in class_name:
#             if cls_n in all_cls:
#                 for obj in root.iter('object'):
#                     if obj.find('difficult'):
#                         difficult = obj.find('difficult').text
#                     else:
#                         difficult = 0
#                     cls = obj.find('name').text
#                     print("cls:", img_name, cls)
#                     if cls not in class_plus.values() or int(difficult) == 1:
#                         continue
#                     cls_id = get_keys(class_plus, cls)[0]
#                     xmlbox = obj.find('bndbox')
#                     b = (
#                     float(xmlbox.find('xmin').text), float(xmlbox.find('ymin').text), float(xmlbox.find('xmax').text)
#                     , float(xmlbox.find('ymax').text))
#                     bb = convert((w, h), b)
#                     label_file.write("{} ".format(cls_id) + " ".join([str(a) for a in bb]) + '\n')
#
# for m in os.listdir(save_label_path):
#     print(len([x for x in open(os.path.join(save_label_path, m)).readlines()]))
#     if len([x for x in open(os.path.join(save_label_path, m)).readlines()]) == 0:  # 标签文件为空删除此文件
#         os.remove(os.path.join('{}'.format(os.path.join(save_label_path, m))))
#     else:
#         img = cv2.imread(os.path.join(orgin_img_path, '{}.jpg'.format(str(m).split('.')[0])))
#         # if m == model[0]:
#         cv2.imwrite(os.path.join(save_img_path, '{}.jpg'.format(str(m).split('.')[0])), img)
# else:
#     cv2.imwrite(os.path.join(save_img_path, model[1], '{}.jpg'.format(str(slabel_file).split('.')[0])), img)

# """划分训练/验证集"""
val_percent = 27  # 划分验证集为57，按照coco数据集比例划分
file_num = len([x for x in os.listdir(save_label_path)])
# print(range(file_num))
val_ran = random.sample(range(file_num), val_percent)
print(val_ran)
img_num = 0
for label in os.listdir(save_label_path):
    img_num += 1
    if img_num in val_ran:
        src1 = os.path.join(save_label_path, label)
        dst1 = os.path.join(divide_label_path, model[1], label)
        Thread(target=shutil.copy, args=[src1, dst1]).start()
        strs = str(label).split('.')[0]
        src2 = os.path.join(save_img_path, '{}.jpg'.format(strs))
        dst2 = os.path.join(divide_img_path, model[1], '{}.jpg'.format(strs))
        Thread(target=shutil.copy, args=[src2, dst2]).start()
    else:
        src1 = os.path.join(save_label_path, label)
        dst1 = os.path.join(divide_label_path, model[0], label)
        Thread(target=shutil.copy, args=[src1, dst1]).start()
        strs = str(label).split('.')[0]
        src2 = os.path.join(save_img_path, '{}.jpg'.format(strs))
        dst2 = os.path.join(divide_img_path, model[0], '{}.jpg'.format(strs))
        Thread(target=shutil.copy, args=[src2, dst2]).start()

