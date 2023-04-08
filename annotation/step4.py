import numpy as np
import os
import yaml
tmp1=[]
tmp2=[]
for label in ["H","I","J"]:
    path = f"I:\\MVAD\\{label}"
    angle1 = os.path.join(path, "angle1")
    angle2 = os.path.join(path, "angle2")
    file_list1 = os.listdir(angle1)
    file_list2 = os.listdir(angle2)
    tmp1 = [f"I:\\MVAD\\{label}\\angle1\\{i}\n" for i in file_list1]
    tmp2 = [f"I:\\MVAD\\{label}\\angle2\\{i}\n" for i in file_list2]
    with open("all_list.txt","a")as f:
        f.write("".join(tmp1))
        f.write("".join(tmp2))
        f.close

#
#
# arg = yaml.load(open(r'./config.yml'), Loader=yaml.FullLoader)
# path=arg['path']
# label=arg['label']
# angle1=os.path.join(path,"angle1")
# angle2=os.path.join(path,"angle2")
# file_list1=os.listdir(angle1)
# file_list2=os.listdir(angle2)
# st1=[f"/home/y202202016/dataset/MVAD/{label}/angle1/{i}\n" for i in file_list1]
# st2=[f"/home/y202202016/dataset/MVAD/{label}/angle2/{i}\n" for i in file_list2]
# with open(os.path.join(path,"list.txt"),"w")as f:
#     f.write("".join(st1))
#     f.write("".join(st2))
#     f.close