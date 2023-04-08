import os
import yaml
arg = yaml.load(open(r'./config.yml'), Loader=yaml.FullLoader)
# GOPR1452_1_2.mp4

# 合并pr导出的文件使用
path=arg['path']
label=arg['label']
file_name_lists= os.listdir(path)
with open("changelog1.txt",'w') as f:
    for i in file_name_lists:
        f.write(os.path.join(path,i.split("嵌套序列 ")[-1].split(".")[0].zfill(2)+".mp4")+","+os.path.join(path,i)+"\n")
        os.rename(os.path.join(path,i),os.path.join(path,i.split("嵌套序列")[-1].split(".")[0].zfill(2)+".mp4"))
    f.close()
file_name_lists= os.listdir(path)
file_name_lists=sorted([int(i.split(".")[0])  for i in file_name_lists])
file_name_lists=[" "+str(i).zfill(2)+".mp4" for i in file_name_lists]
angle1=os.path.join(path,"angle1")
angle2=os.path.join(path,"angle2")
if not os.path.exists(angle1):
    os.makedirs(angle1)
if not os.path.exists(angle2):
    os.makedirs(angle2)
flag=1
angle1_count=1
angle2_count=1
with open("changelog2.txt",'w') as f:
    for i in file_name_lists:
        if flag==1:
            flag=2
            f.write(os.path.join(angle1,label+"1_"+str(angle1_count).zfill(2)+".mp4")+","+os.path.join(path,i)+"\n")
            os.rename(os.path.join(path,i),os.path.join(angle1,label+"1_"+str(angle1_count).zfill(2)+".mp4"))
            angle1_count+=1
        else :
            flag=1
            os.rename(os.path.join(path,i),os.path.join(angle2,label+"2_"+str(angle2_count).zfill(2)+".mp4"))
            angle2_count+=1
    f.close()
    print("CHANGE SUCCESS!")