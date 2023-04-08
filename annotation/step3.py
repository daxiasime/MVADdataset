import numpy as np
import os
import yaml
arg = yaml.load(open(r'./config.yml'), Loader=yaml.FullLoader)
path,label=arg['path'],arg['label']
annotation_path=os.path.join(path,"annotation_file")
annotation_list=os.listdir(annotation_path)
angle1=os.path.join(path,"angle1")
angle2=os.path.join(path,"angle2")
file_list1=[os.path.join(angle1,i) for  i in os.listdir(angle1)]
file_list2=[os.path.join(angle2,i) for  i in os.listdir(angle2)]
file_list=file_list1+file_list2
data=[]
type_log={}
with open(os.path.join(path,"type_log.txt"),"r") as f:
    data=f.readlines()
    f.close()
for ele in data:
    i=ele.split(",")
    type_log[i[0]]=i[1].strip()


for i in file_list:
    data=np.load(os.path.join(annotation_path,i.split("\\")[-1].split(".")[0]+".npy"))
    na=i.split("\\")[-1].split(".")[0]
    pre_path="\\".join(i.split("\\")[:-1])
    if np.sum(data,axis=0)[1]==0:
        name=na+"_0_"+type_log[na+".mp4"]
        new_name=os.path.join(annotation_path,name+ ".npy")
        os.rename(os.path.join(annotation_path, na+".npy"),new_name )
        new_name=os.path.join(pre_path, name + ".mp4")
        os.rename(i,new_name)
    else:
        name = na + "_1_" + type_log[na + ".mp4"]
        new_name = os.path.join(annotation_path, name + ".npy")
        os.rename(os.path.join(annotation_path, na + ".npy"), new_name)
        new_name = os.path.join(pre_path, name + ".mp4")
        os.rename(i, new_name)
