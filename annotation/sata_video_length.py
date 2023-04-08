# coding:utf-8

import os
import cv2

import pandas as pd
import matplotlib.pyplot as plt

import seaborn as sns
anno_all=[]

for label in ["H","I","J"]:
    video_dir = rf"I:\MVAD\{label}\angle1"
    for filename in os.listdir(video_dir):
        if filename.endswith('.mp4') or filename.endswith('.avi'):
            filepath = os.path.join(video_dir, filename)
            cap = cv2.VideoCapture(filepath)
            length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            duration = length / fps
            if duration>200:
                print(filename)
            anno_all.append(int(duration))
            cap.release()

import matplotlib.pyplot as plt

# 计算数量
count_less_20 = len([x for x in anno_all if   x < 20])*2
count_less_40 = len([x for x in anno_all if  20 <= x < 40])*2
count_less_60 = len([x for x in anno_all if  40 <= x < 60])*2
count_less_80 = len([x for x in anno_all if  60 <= x < 80])*2
count_less_100 = len([x for x in anno_all if  80 <= x < 100])*2
count_less_120 = len([x for x in anno_all if  100 <= x < 120])*2
count_less_140 = len([x for x in anno_all if  120 <= x < 140])*2
count_less_160 = len([x for x in anno_all if  140 <= x < 160])*2
count_less_180 = len([x for x in anno_all if   x > 160])*2

# 绘制柱状图
labels = ['<20','20-40','40-60',
          '60-80', '80-100','100-120',
          '120-140','140-160','>160']
counts = [count_less_20, count_less_40, count_less_60,
            count_less_80, count_less_100,count_less_120,
            count_less_140, count_less_160,count_less_180

          ]
print(sum(anno_all)*2/60,sum(anno_all)*2/3600)
hatches = ['/', '.', 'x']  # 设置不同区间的填充图案
plt.figure(dpi=300)
plt.subplots_adjust(left=0.13,  bottom=0.22)
plt.bar(labels, counts, hatch="///", color='white', edgecolor='black')  # 设置柱形图颜色和边框颜色
# plt.bar(labels, counts)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
# plt.title('视频时长分布图',size=14)
plt.ylim(0,200)
plt.xlabel('视频时长（s）',size=14)
plt.ylabel('视频数量',size=14)
plt.xticks(rotation=45)
for i, v in enumerate(counts):
    if v >1:
        plt.text(i, v+0.7, str(v), ha='center',size=14)
plt.savefig("video_length")

