"""从coco中提取某些类，有点冗余，还未找到解决办法"""

import os
import cv2

# the path you want to save your results for coco to x
savepath = "F:/mutil_coco/"
train_img_dir = savepath + 'images/train/'
test_img_dir = savepath + 'images/val/'
label_dir = savepath + 'labels/'

# the orgin image path
orgin_img_path = 'F:/coco2017/'
orgin_label_path = 'C:/Users/Administrator/Desktop/coco/labels/'
datasets_list = ['train2017', 'val2017']  #

# the class you want to extract
classes_names = ['train', 'person', 'bicycle', 'car', 'motorcycle', 'bus', 'truck', 'bench', 'cat', 'bird', 'dog',
                 'sheep', 'backpack', 'umbrella', 'handbag', 'suitcase', 'sports ball', 'kite', 'baseball bat',
                 'skateboard', 'tennis racket', 'bottle', 'wine glass', 'cup', 'bowl', 'chair', 'potted plant',
                 'cell phone', 'book', 'clock', 'vase']  # 0
# all class
all_class = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light',
             'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
             'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
             'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard',
             'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
             'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
             'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard',
             'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors',
             'teddy bear', 'hair drier', 'toothbrush']
# 求所需类别的索引
indexes = ['{}'.format(all_class.index(classes_names[i])) for i in range(len(classes_names))]
# print(indexes)

# 提取某一类并写道另一个文件夹里
print("转换标签")
for cls_label in os.listdir(orgin_label_path):  # 得到原始labels文件夹里的所有文件
    if cls_label in datasets_list:  # 只使用train2017和val2017文件夹
        for label_files in os.listdir(os.path.join(orgin_label_path, cls_label)):  # 列出原始labels/train里的文件
            # 打开原始labels/train里的文件
            with open(os.path.join(orgin_label_path, cls_label, label_files), 'r') as label_file:
                label_line = label_file.readlines()  # 按行读取文件
                if len(label_line) > 0:  # 文件不为空
                    with open(os.path.join(label_dir, cls_label, label_files), 'w') as f:  # 打开准备好的标签文件
                        for i in range(len(label_line)):
                            if label_line[i].split(" ")[0] in indexes:  # 按标签索引写入
                                label_index = '{}'.format(indexes.index(label_line[i].split(" ")[0]))
                                f.write("{} {} {} {} {}".format(label_index, label_line[i].split(" ")[1], label_line[i].split(" ")[2], label_line[i].split(" ")[3], label_line[i].split(" ")[4]))


# # 筛选一些遗漏的空文件
print("筛选文件")
for datasets in datasets_list:  # 分别选择训练集和测试集
    for _label_file in os.listdir(os.path.join(label_dir, datasets)):  # 标签文件
        if os.path.getsize(os.path.join(label_dir, datasets, _label_file)) == 0:  # 标签文件为空删除此文件
            os.remove(os.path.join(label_dir, datasets, _label_file))

# 把对应的图片也保存到另一个文件夹
print("保存图片")
for datasets in datasets_list:  # 分别选择训练集和测试集
    for _label_file in os.listdir(os.path.join(label_dir, datasets)):
        img_name = str(_label_file).split(".")[0] + '.jpg'  # 根据标签写出图片名
        img = cv2.imread(os.path.join(orgin_img_path, datasets, img_name))  # 打开图片
        if datasets == 'train2017':  # 分别写入对应文件夹
            cv2.imwrite(os.path.join(train_img_dir, img_name), img)
        else:
            cv2.imwrite(os.path.join(test_img_dir, img_name), img)
