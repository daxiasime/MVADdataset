"""
1.视频总数
2.正常视频数
3.异常视频数
4.正常视频帧数
5.异常视频帧数
6.视频帧数
7.视频时长
8.视频帧大小
9.异常类型
"""
import warnings

warnings.filterwarnings('ignore')

import pandas as pd
import matplotlib.pyplot as plt


import os
import pandas as pd
import numpy as np
data=[]
address=[]
with open("./all_list.txt","r") as f:
    address=f.readlines()
    f.close()
data=address
data=[i.strip().split("\\")[-1].split(".")[0] for i in data]
df_list=[]
for i in data:
    tmp=i.split("_")
    df_list.append([tmp[0][0],tmp[0]+"_"+tmp[1],tmp[2],tmp[3],tmp[4],tmp[5]])
df=pd.DataFrame(df_list,columns=["label","file_name","Abnomal","Cycling","Car","Drag"])



dic={}
# 查看总的
for i in data:
    tmp=i.split("_")
    name=tmp[0][0]+tmp[1]
    A=1 if tmp[3]=="A" else 0
    B=1 if tmp[4]=="B" else 0
    C=1 if tmp[5]=="C" else 0
    if name in dic:
        dic[name][1]+=int(tmp[2])
        dic[name][2]+=A
        dic[name][3]+=B
        dic[name][4]+=C
    else:
        dic[name]=[name,int(tmp[2]),A,B,C]



df=pd.DataFrame(df_list,columns=["label","file_name","Abnomal","Cycling","Car","Drag"])
df_merage=pd.DataFrame(dic.values(),columns=["name","Abnomal","Cycling","Car","Drag"])
print(df_merage["Abnomal"].value_counts())
df=df_merage
df['Cycling']=df['Cycling'].replace("O",0)
df['Cycling']=df['Cycling'].replace("A",1)
df['Car']=df['Car'].replace("B",1)
df['Car']=df['Car'].replace("O",0)
df['Drag']=df['Drag'].replace("C",1)
df['Drag']=df['Drag'].replace("O",0)
print(df["Abnomal"].value_counts())
print("骑行异常",df["Cycling"].sum())
print("汽车异常",df["Car"].sum())
print("拖拉异常",df["Drag"].sum())
# print(df["label"].value_counts())
print("去重后的骑车异常",df[df["Cycling"]==1][df["Car"]==0][df["Drag"]==0].shape)
print("去重后的汽车异常",df[df["Cycling"]==0][df["Car"]==1][df["Drag"]==0].shape)
print("去重后的拖拉异常",df[df["Cycling"]==0][df["Car"]==0][df["Drag"]==1].shape)

print("正常视频")
nor=[f"{i[0]},{i[1]},{i[2]},{i[3]},{i[4]}\n"  for  i in list(df[df["Abnomal"]==0].values) ]
abnor1=[f"{i[0]},{i[1]},{i[2]},{i[3]},{i[4]}\n" for  i in list(df[df["Abnomal"]==1].values)]
abnor2=[f"{i[0]},{i[1]},{i[2]},{i[3]},{i[4]}\n" for  i in list(df[df["Abnomal"]==2].values)]
with open("video_list.txt", "w") as f:
    f.write("".join(nor))
    f.write("".join(abnor1))
    f.write("".join(abnor2))
f.close()
print(nor)

# exit()

bar_data=[]



bar_data.append([df["Cycling"].sum(),df[df["Cycling"]==1][df["Car"]==0][df["Drag"]==0].shape[0],"骑行"])

bar_data.append([df["Car"].sum(),df[df["Cycling"]==0][df["Car"]==1][df["Drag"]==0].shape[0],"开车"])

bar_data.append([df["Drag"].sum(),df[df["Cycling"]==0][df["Car"]==0][df["Drag"]==1].shape[0],"拖动"])
bar_data=pd.DataFrame(bar_data,columns=["包含重复视频","不包含重复视频","label"])



import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import MaxNLocator



plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))

stat = []
for i in address:
    name=i.strip().split("\\")[-1].split(".")[0]
    path=""
    tmp = i.split("\\")[:-2]
    for ele in tmp:
        path+=(ele+"\\")
    path=path+"annotation_file"
    data = np.load(os.path.join(path,name+".npy"))
    if data.sum(axis=0)[1]!=0:
        stat.append(round(data.sum(axis=0)[1]/data.shape[0]*100,2))


plt.figure(dpi=220)
# sns.set_style("dark", {"axes.facecolor": "#e9f3ea"})#修改背景


# 计算数量
count_less_10 = len([x for x in stat if   x < 10])
count_less_20 = len([x for x in stat if  10 <= x < 20])
count_less_30 = len([x for x in stat if  20 <= x < 30])
count_less_40 = len([x for x in stat if  30 <= x < 40])
count_less_50 = len([x for x in stat if  40 <= x < 50])
count_less_60 = len([x for x in stat if  50 <= x < 60])
count_less_70 = len([x for x in stat if  60 <= x < 70])
count_less_80 = len([x for x in stat if  70 <= x < 80])
count_less_90 = len([x for x in stat if  80 <= x < 90])
count_less_100 = len([x for x in stat if  90 <= x < 100])


# 绘制柱状图
labels = ['0-10','10-20','20-30',
          '30-40', '40-50','50-60',
          '60-70','70-80','80-90','90-100']
counts = [count_less_10, count_less_20, count_less_30,count_less_40,
            count_less_50, count_less_60,count_less_70,count_less_80,
            count_less_90, count_less_100
          ]
hatches = ['/', '.', 'x']  # 设置不同区间的填充图案
plt.figure(dpi=300)
plt.subplots_adjust(left=0.14,  bottom=0.2)
plt.bar(labels, counts, hatch="xxx", color='white', edgecolor='black')  # 设置柱形图颜色和边框颜色
# plt.bar(labels, counts)
# plt.title('异常视频中异常视频帧占比',size=14)
plt.ylim(0,200)
plt.xlabel('异常视频帧占比（%）',size=14)
plt.ylabel('视频数量',size=14)
plt.xticks(rotation=45)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
for i, v in enumerate(counts):
    if v >1:
        plt.text(i, v+0.9, str(v), ha='center',fontsize=14)
plt.savefig("anno_frame_dis")




#
# x_data =["nodesTotalNumber", "totalPathLength", "pathNodesNumber", "NodeUtilization", "time"]
# Y1 = bar_data["包含重复视频"]
# Y2 = bar_data["不包含重复视频"]
# bar_width = 0.35
#
# m =np.arange(3)
#
# a=plt.bar(x=m, height=Y1, label="包含重复视频", align='center',width=bar_width,hatch="//",color="w",edgecolor="k")
#
# b=plt.bar(x=m + bar_width+0.05, height=Y2,
#         label="不包含重复视频",
#         width=bar_width,
#         align='center',
#         hatch="||",
#         color="w",
#         edgecolor="k")
#
# plt.text(-0.05, 1.03*273-6, '%d' % float(273))
# plt.text(0.35, 1.03*224-5, '%d' % float(224))
# plt.text(0.95, 1.03*103, '%d' % float(103))
# plt.text(1.35, 1.03*59, '%d' % float(59))
# plt.text(1.95, 1.03*67, '%d' % float(67))
# plt.text(2.35, 1.03*45, '%d' % float(45))
#
# plt.xticks([0.2,1.2,2.2], ["骑车", "机动车", "拖行"])
#
# # 设置横坐标和纵坐标的标题
# plt.xlabel('异常类型')
# plt.ylabel('出现次数')
# plt.ylim(0,350)
# plt.legend()
# plt.title('MA-VAD数据集异常类型表\n',fontsize= '12')
# # 设置图表移动
# f = plt.gcf()
# # f.subplots_adjust(left=0.2,bottom=0.42) # 可以调整图片的位置
# plt.savefig("异常类型表.png",dpi=200,bbox_inches="tight")
# plt.show()
