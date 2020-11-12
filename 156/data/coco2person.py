"""从coco中提取某一类（person） 有点冗余，还未找到解决办法"""

import os
import cv2

# the path you want to save your results for coco to person
savepath = "F:/cocoperson/"
train_img_dir = savepath + 'images/train/'
test_img_dir = savepath + 'images/val/'
label_dir = savepath + 'labels/'

orgin_img_path = 'F:/coco2017/'
orgin_label_path = 'F:/coco/labels/'
datasets_list = ['train2017', 'val2017']  #

classes_names = ['person']  # 0
# 提取某一类并写道另一个文件夹里
print("转换标签")
for cls_label in os.listdir(orgin_label_path):
    if cls_label in datasets_list:
        print("cls_label", cls_label)
        for label_files in os.listdir(os.path.join(orgin_label_path, cls_label)):
            with open(os.path.join(orgin_label_path, cls_label, label_files), 'r') as label_file:
                print("os.path.join(orgin_label_path, cls_label, label_files)", os.path.join(orgin_label_path, cls_label, label_files))
                label_line = label_file.readlines()
                if len(label_line) > 0:
                    with open(os.path.join(label_dir, cls_label, label_files), 'w') as f:
                        for i in range(len(label_line)):
                            if label_line[i][0] == '0':
                                f.write(label_line[i])
                                # print(label_line[i])

# 筛选一些遗漏的空文件
print("筛选文件")
for datasets in datasets_list:
    for _label_file in os.listdir(os.path.join(label_dir, datasets)):
        if os.path.getsize(os.path.join(label_dir, datasets, _label_file)) == 0:
            os.remove(os.path.join(label_dir, datasets, _label_file))

# 把对应的图片也保存到另一个文件夹
# print("保存图片")
# for datasets in datasets_list:
#     for _label_file in os.listdir(os.path.join(label_dir, datasets)):
#         img_name = str(_label_file).split(".")[0] + '.jpg'
#         img = cv2.imread(os.path.join(orgin_img_path, datasets, img_name))
#         # if datasets == 'train2017':
#         #     cv2.imwrite(os.path.join(train_img_dir, img_name), img)
#         # else:
#         cv2.imwrite(os.path.join(test_img_dir, img_name), img)
#



