import csv
import threading
import random
import os
import glob
import shutil
from tqdm import tqdm, trange
from collections import defaultdict
from threading import Thread
# 真实情况
csv_path = 'F:/test/train-remove-bbox.csv'  # 需要解剖的csv文件
txt_path = 'F:/38cls_open-image/labels/'  # 存放新建的一系列txt文件的文件夹
orgin_img_path = 'G:/Open_Images_Dataset/train/'
save_img_path = 'F:/38cls_open-image/images/'

divide_img_path = 'F:/mutil_open-image/images/'
divide_label_path = 'F:/mutil_open-image/labels/'

model = ['train', 'val']

# 测试情况
# csv_path = 'C:/Users/Administrator/Desktop/test1.csv'  # 需要解剖的csv文件
# txt_path = 'F:/test/'  # 存放新建的一系列txt文件的文件夹
# orgin_img_path = 'G:/Open_Images_Dataset/train/'
# save_img_path = 'F:/test/'

all_label = {0: '/m/07jdr', 1: '/m/01g317', 2: '/m/0199g', 3: '/m/0k4j', 4: '/m/04_sv', 5: '/m/01bjv', 6: '/m/07r04',
             7: '/m/0cvnqh', 8: '/m/01yrx', 9: '/m/015p6', 10: '/m/0bt9lr', 11: '/m/07bgp', 12: '/m/01940j',
             13: '/m/0hnnb', 14: '/m/080hkjn', 15: '/m/01s55n', 16: '/m/018xm', 17: '/m/02zt3', 18: '/m/03g8mr',
             19: '/m/06_fw', 20: '/m/0h8my_4', 21: '/m/04dr76w', 22: '/m/09tvcd', 23: '/m/02p5f1q', 24: '/m/03hj559',
             25: '/m/01mzpv', 26: '/m/03fp41', 27: '/m/050k8', 28: '/m/0bt_c3', 29: '/m/01x3z', 30: '/m/02s195',
             31: '/m/07c52', 32: '/m/0zvk5', 33: '/m/02dgv', 34: '/m/025dyy', 35: '/m/018p4k', 36: '/m/01j51'}
class_name = {'/m/0zvk5', '/m/02dgv', '/m/025dyy', '/m/018p4k', '/m/01j51'}


def get_keys(d, value):
    # return [k for k, v in d.items() if v == value]
    # print("list(d.keys())[list(d.values()).index(value)]", list(d.keys())[list(d.values()).index(value)])
    return list(d.keys())[list(d.values()).index(value)]


def convert(box):  # 坐标归一化
    x = (box[0] + box[1]) / 2.
    y = (box[2] + box[3]) / 2.
    w = box[1] - box[0]
    h = box[3] - box[2]
    return ("%.6f" % x, "%.6f" % y, "%.6f" % w, "%.6f" % h)  # 集合是无序的


def Recive():
    return csv.DictReader(open(csv_path, 'r'))


def file_processing():
    tqdm.monitor_interval = 0
    dict_reader = Recive()
    result = defaultdict()  # 图片对应过个标签
    label = set()  # 多个标签
    img = set()  # 图片
    print('读标签')
    for i in tqdm(dict_reader):
        if i['ImageID'] not in img:
            img.add(i['ImageID'])  # 图片没出现过 就放进去
            label = {i['LabelName']}  # 标签list初始化
        else:
            # if i['LabelName'] not in label:
            label.add(i['LabelName'])  # 没出现过的标签就放里面
        result[i['ImageID']] = label  # 标签和图片对应放到字典里
    # print('result', result)
    print("保存图片名")
    img_re = set()
    x_v = list(result.values())
    for i in trange(len(result)):
        if x_v[i] & class_name:
            img_re.add(str(get_keys(result, x_v[i])))
    return img_re


def read_txt():
    tqdm.monitor_interval = 0
    dict_reader = Recive()
    img_re = file_processing()
    print("写文件")
    for i in tqdm(dict_reader):
            if i['ImageID'] in img_re:  # 图片是我要的
                file = os.path.join(txt_path, "{}.txt".format(i['ImageID']))
                with open(file, 'a+') as f:  # 打开文件（追加写入法）
                    if i['LabelName'] in all_label.values():
                        cls = str(get_keys(all_label, i['LabelName']))
                        print("cls", cls)
                        if len(cls) == 0:
                            continue
                        b = (float(i['XMin']), float(i['XMax']), float(i['YMin']), float(i['YMax']))
                        box = convert(b)
                        f.write('{} '.format(cls) + ' '.join([a for a in box]) + '\n')  # 写入内容


def img_processing():
    tqdm.monitor_interval = 0
    img_str = file_processing()
    # print("img_str", img_str)
    print('复制图片')
    for img_name in img_str:
        orgin = glob.glob(os.path.join(orgin_img_path, r'train_0*/{}.jpg'.format(img_name)))
        if len(orgin) != 0:
            save = os.path.join(save_img_path, r"{}.jpg".format(str(img_name)))
            shutil.copy(str(orgin[0]), str(save))
        else:
            print("   ", os.path.join(orgin_img_path, r'train_0*/{}.jpg'.format(str(img_name))))
            os.remove(os.path.join(txt_path, "{}.txt".format(str(img_name))))
def divide_file():
    val_percent = 305  # 划分验证集为305，按照coco数据集比例划分
    file_num = len([x for x in os.listdir(txt_path)])
    # print(range(file_num))
    val_ran = random.sample(range(file_num), val_percent)
    print(val_ran)
    img_num = 0
    for label in os.listdir(txt_path):
        with open(os.path.join(txt_path, label), 'r') as f:
            pass
        f.close()
        img_num += 1
        if img_num in val_ran:
            src1 = os.path.join(txt_path, label)
            dst1 = os.path.join(divide_label_path, model[1], label)
            shutil.copy(src1, dst1)
            strs = str(label).split('.')[0]
            src2 = os.path.join(save_img_path, '{}.jpg'.format(strs))
            dst2 = os.path.join(divide_img_path, model[1], '{}.jpg'.format(strs))
            shutil.copy(src2, dst2)
        else:
            src1 = os.path.join(txt_path, label)
            dst1 = os.path.join(divide_label_path, model[0], label)
            shutil.copy(src1, dst1)
            strs = str(label).split('.')[0]
            src2 = os.path.join(save_img_path, '{}.jpg'.format(strs))
            dst2 = os.path.join(divide_img_path, model[0], '{}.jpg'.format(strs))
            shutil.copy(src2, dst2)


if __name__ == '__main__':
    divide_file()
    # p1 = threading.Thread(target=Recive)
    # p3 = threading.Thread(target=read_txt)
    # p2 = threading.Thread(target=img_processing)
    # p1.start()
    # p3.start()
    # p2.start()
