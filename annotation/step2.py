import cv2
import numpy as np
import keyboard #Using module keyboard
import yaml
# 标注文件的时候使用的
def get_loc(img,data,cnt):
    a =[]
    b = []
    erro=0
    frame=0
    def on_EVENT_LBUTTONDOWN(event, x, y,flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            xy = "%d,%d" % (x, y)
            a.append(x)
            b.append(y)
            cv2.circle(img, (x, y), 2, (255, 0, 0), thickness=3)
            cv2.putText(img, xy, (x, y), cv2.FONT_HERSHEY_PLAIN,
                        1.0, (0, 0, 0), thickness=1)
            cv2.imshow("image", img)

    cv2.namedWindow("image")
    cv2.setMouseCallback("image", on_EVENT_LBUTTONDOWN)
    cv2.imshow("image", img)
    cv2.waitKey(0)
    if len(a)==2and len(b)==2:
        print(a[0],b[0])
        erro=1
        cv2.rectangle(img,  # 图片
                      (a[0], b[0]),  # (xmin, ymin)左上角坐标
                      (a[1], b[1]),  # (xmax, ymax)右下角坐标
                      (0, 255, 0), 1)  # 颜色，线条宽度
        # img[b[0]:b[1],a[0]:a[1],:] = 0   #注意是 行，列（y轴的，X轴）
        cv2.imshow("image", img)
        cv2.waitKey(0)
        data[cnt][1]=erro
        data[cnt][2]=a[0]
        data[cnt][3]=b[0]
        data[cnt][4]=a[1]
        data[cnt][5]=b[1]
    return data



def video_biaozhu(file_path,annotation_path,name,):
    video_path=os.path.join(file_path,name)
    cap = cv2.VideoCapture(video_path)
    max_frame = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    # 判断是否存在npy文件
    annotation_file_path=os.path.join(annotation_path,name.split(".mp4")[0]+".npy")
    if os.path.exists(annotation_file_path):
        data = np.load(annotation_file_path).tolist()
    else:
        data = []
        # 直接创建一个矩阵
        for i in range(int(max_frame)):
            data.append([i, 0, 0, 0, 0, 0])
    print(len(data),len(data[0]))
    cnt=0
    flag = True
    save = False
    clear = False

    a1,b1,c1=tuple(type_log[name])
    while   flag:
        if cnt>=max_frame or cnt<0:
            break
        cap.set(cv2.CAP_PROP_POS_FRAMES, cnt)
        ret, frame = cap.read()
        cv2.putText(frame, "frame :"+str(cnt).zfill(len(str(int(max_frame))))+"|"+str(int(max_frame)), (320, 50), cv2.FONT_HERSHEY_PLAIN,
                    2.0, (255, 102, 0), thickness=3)
        cv2.putText(frame, "file :"+name, (720, 50), cv2.FONT_HERSHEY_PLAIN,
                    2.0, (255, 102, 0), thickness=3)
        # 计算长度
        width=1280/max_frame
        pt=[]
        for i in range(int(max_frame)):
            pt.append([int(i*width),650-data[i][1]*50])
        # cv2.line(img=frame, pt, color=(0, 255, 255), thickness=5)
        pts = np.array(pt, np.int32)
        # reshape的第一个参数为-1，表明这一维度是根据后边算出来的
        pts.reshape((-1, 1, 2))
        cv2.polylines(frame, [pts], False, (0, 255, 255))
        cv2.circle(frame, (int(cnt*width),650-data[cnt][1]*50 ), 2, (255, 0, 0), thickness=3)

        # 绘制异常类型标注(0,128,0)
        cv2.putText(frame, "A", (110, 340), cv2.FONT_HERSHEY_PLAIN, 2.0,(255, 0, 0), thickness=2)
        cv2.putText(frame, "B", (150, 340), cv2.FONT_HERSHEY_PLAIN, 2.0,(255, 0, 0), thickness=2)
        cv2.putText(frame, "C", (190, 340), cv2.FONT_HERSHEY_PLAIN, 2.0,(255, 0, 0), thickness=2)
        if a1=="A":
            cv2.circle(frame, (120, 300), 5, (0,0,255), thickness=8)
        elif a1=="O":
            cv2.circle(frame, (120, 300), 5, (0, 128, 0), thickness=8)
        if b1=="B":
            cv2.circle(frame, (160, 300), 5, (0,0,255), thickness=8)
        elif b1=="O":
            cv2.circle(frame, (160, 300), 5, (0, 128, 0), thickness=8)
        if c1=="C":
            cv2.circle(frame, (200, 300), 5, (0,0,255), thickness=8)
        elif c1=="O":
            cv2.circle(frame, (200, 300), 5, (0, 128, 0), thickness=8)

        if clear:
            data[cnt][1]=0
            data[cnt][2]=0
            data[cnt][3]=0
            data[cnt][4]=0
            data[cnt][5]=0

            cv2.putText(frame, "clear success ！", (800, 360), cv2.FONT_HERSHEY_PLAIN, 2.0,
                        (131, 185, 66), thickness=3)
            clear=False

        cv2.rectangle(frame,  # 图片
                      (data[cnt][2], data[cnt][3]),  # (xmin, ymin)左上角坐标
                      (data[cnt][4], data[cnt][5]),  # (xmax, ymax)右下角坐标
                      (0, 255, 0), 1)  # 颜色，线条宽度
        # cv2.putText(frame, "<-A,S->  5<-D,F->5      <-Q,W->  15<-E,R->15 ",(250, 700), cv2.FONT_HERSHEY_PLAIN,2.0, (0, 0, 0), thickness=3)
        if save:
            cv2.putText(frame, "save success ！", (800, 360), cv2.FONT_HERSHEY_PLAIN, 2.0,
                        (131, 185, 66), thickness=3)
            save=False

        cv2.imshow("image", frame)
        data=get_loc(frame,data,cnt) #进行标注
        tmp = data[cnt]


        while True:  # making a loop

            if keyboard.is_pressed('a'):  # if key 'a' is pressed
                cnt-=1
                if cnt  >= 0:
                    data[cnt] = tmp
                break
            elif keyboard.is_pressed('s'):  # if key 'a' is pressed
                cnt+=1
                if cnt < max_frame:
                    data[cnt] = tmp
                break
            elif keyboard.is_pressed('q'):  # 表示第一种异常是否存在
                if a1=="A":
                    a1="O"
                    print("set a = 0")
                    break
                elif a1=="O" :
                    a1="A"
                    print("set a = 1")
                    break

            elif keyboard.is_pressed('w'):  # 表示第二种异常是否存在
                if b1=="B":
                    b1="O"
                    print("set b = 0")
                else :
                    b1="B"
                    print("set b = 1")
                break
            elif keyboard.is_pressed('e'):  # 表示第三种异常是否存在
                if c1=="C":
                    c1="O"
                    print("set c = 0")
                else :
                    c1="C"
                    print("set c = 1")
                break
            elif keyboard.is_pressed('r'):  # if key 'a' is pressed
                cnt+=15
                break
            elif keyboard.is_pressed('h'):  # if key 'a' is pressed
                cnt-=150
                break
            elif keyboard.is_pressed('j'):  # if key 'a' is pressed
                cnt+=150
                break
            elif keyboard.is_pressed('o'):  # if key 'a' is pressed
                clear=True
                break
            elif keyboard.is_pressed('l'):  # if key 'a' is pressed
                print("保存成功！")
                np.save(annotation_file_path, np.array(data))
                save=True
                break
            elif keyboard.is_pressed('d'):  # if key 'a' is pressed
                print('后进5复制')

                for i in range(5):
                    if cnt-i>=0:
                        data[cnt-i]=tmp
                cnt-=5
                break
            elif keyboard.is_pressed('f'):  # if key 'a' is pressed
                print('前进15复制')
                tmp=data[cnt]
                for i in range(5):
                    if cnt+i<max_frame:
                        data[cnt+i]=tmp
                cnt+=5
                break
            elif keyboard.is_pressed('p'):  # if key 'a' is pressed
                print('next file')
                flag=False
                break
            else:
                break


        # (帧,是否异常，)
        np.save(annotation_file_path, np.array(data))
        # a.append([i,res[0],res[1],res[2],res[3],res[4]])
    cap.release()
    cv2.destroyAllWindows()

    type_log[name]=[a1,b1,c1]

import os
arg = yaml.load(open(r'./config.yml'), Loader=yaml.FullLoader)
path=arg['path']
label=arg['label']
path=path
annotation_path=os.path.join(path,"annotation_file")
if not os.path.exists(annotation_path):
    os.makedirs(annotation_path)
angle1=os.path.join(path,"angle1")
angle2=os.path.join(path,"angle2")
file_list1=os.listdir(angle1)
file_list2=os.listdir(angle2)
type_log={}
if not os.path.exists(os.path.join(path,"type_log.txt")):
    with open(os.path.join(path, "type_log.txt"), "w") as f:
        f.write("")
        f.close()

with open(os.path.join(path,"type_log.txt"),"r") as f:
    data=f.readlines()
    f.close()
for ele in data:
    i=ele.split(",")
    type_log[i[0]]=i[1].strip().split("_")


for name in file_list1:
    print("处理"+name)
    if name not in type_log.keys():
        type_log[name]=["O","O","O"]
    video_biaozhu(angle1,annotation_path,name)
    with open(os.path.join(path, "type_log.txt"), "w") as f1:
        for name in type_log.keys():
            f1.write(name + "," + "_".join(type_log[name]) + "\n")
        f1.close()
for name in file_list2:
    print("处理"+name)
    if name not in type_log.keys():
        type_log[name]=["O","O","O"]
    video_biaozhu(angle2,annotation_path,name)
    with open(os.path.join(path, "type_log.txt"), "w") as f1:
        for name in type_log.keys():
            f1.write(name + "," + "_".join(type_log[name]) + "\n")
        f1.close()



