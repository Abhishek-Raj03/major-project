import cv2
import mediapipe as mp
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
mp_drawing_styles=mp.solutions.drawing_styles
import time
import pandas as pd
import csv
from datetime import date

def push(id_1):
    count=0
    position=None
    cap = cv2.VideoCapture(0)
    start=time.time()
    with mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7) as pose:
        while cap.isOpened():
            success,image=cap.read()
            if not success:
                print("Empty Camera")
                break
                
    #         # Recolor image to RGB
    #         image = cv2.cvtColor(cv2.flip(image,1), cv2.COLOR_BGR2RGB)
            
    #         # Make detection
    #         result = pose.process(image)
            
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
        
            # Make detection
            result = pose.process(image)

            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            imlist=[]
            
            if result.pose_landmarks:
                mp_drawing.draw_landmarks(
                image,result.pose_landmarks,mp_pose.POSE_CONNECTIONS)
                for id,im in enumerate(result.pose_landmarks.landmark):
                    h,w,_=image.shape
                    X,Y=int(im.x*w),int(im.y*h)
                    imlist.append([id,X,Y])
            if len(imlist)!=0:      
                if ((imlist[12][2] - imlist[14][2])>=-100 and (imlist[11][2] - imlist[13][2])>=-100):
                    position = "down"
                
                if ((imlist[12][2] - imlist[14][2])<=-100 and (imlist[11][2] - imlist[13][2])<=-100) and position == "down":
                    position = "up"
                    count +=1 
                    print(count)
                    
                # Render curl counter
                # Setup status box
                cv2.rectangle(image, (0,0), (200,73), (255,255,255), -1)
                cv2.putText(image, 'Num Pushups', (15,12), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,153,0), 1, cv2.LINE_AA)
                cv2.putText(image, str(count),
                        (30,60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)
                
    #         cv2.imshow("Push up counter",cv2.flip(image,1))
            resized = cv2.resize(image, (1200,850), interpolation = cv2.INTER_AREA)
            cv2.imshow("Push up counter",resized)
            key=cv2.waitKey(1)
            if key==ord('q'):
                break
            
    cap.release()
    cv2.destroyAllWindows()
    end=time.time()
    # print("-----------------------"+str(id)+"--------------------")
    df=pd.read_csv('users.csv')
    id_1=int(id_1)
    id_1=id_1-1
    # print(id)
    df.loc[id_1,'time']=df.loc[id_1,'time']+int((end-start)/60)
    df.loc[id_1,'calorie_burnt']=df.loc[id_1,'calorie_burnt']+count*2 # for 1count 2cal burn
    df.to_csv('users.csv',index=False)

    id1=id_1+1
    row1=-1
    c=0
    with open('daily.csv') as o:
        myData=csv.reader(o)
        for row in myData:
            if str(row[0])+str(row[2])==str(id1)+str(date.today()):
                f=1
                row1=c
                break
            c+=1
    row1-=1
    # print("-----------------"+str(row1)+"------------------")
    if row1>=0:
        df1=pd.read_csv('daily.csv')
        df1.loc[row1,'time']=df1.loc[row1,'time']+int((end-start)/60)
        df1.loc[row1,'calorie']=df1.loc[row1,'calorie']+count*2
        df1.to_csv('daily.csv',index=False)
    else:
        csv_writer=csv.writer(open('daily.csv','a',newline=""))
        lis=[id1,df.loc[id,'name'],date.today(),int((end-start)/60),count*2]
        csv_writer.writerow(lis)