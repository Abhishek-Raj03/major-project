import cv2
import mediapipe as mp
import time
import numpy as np
import pandas as pd
from datetime import date
import math
# from app import id
import csv
# from celluloid import Camera
# import pyshine as ps
# from calc_angle import calculateAngle,Average,convert_data,dif_compare,diff_compare_angle
# from extract_keypoints import extractKeypoint
# from compare_pose import compare_pose
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def calculate_angle(a,b,c):
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
        
    return angle

def dumb(id):
    cap = cv2.VideoCapture(0)

    # Curl counter variables
    counter = 0 
    stage = None
    a=0
    start=time.time()
    ## Setup mediapipe instance
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            # print(a)
            # a+=1
            ret, frame = cap.read()
            
            # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
        
            # Make detection
            results = pose.process(image)
        
            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark
                
                # Get coordinates
                shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                
                # Calculate angle
                angle = calculate_angle(shoulder, elbow, wrist)
                
                # Visualize angle
                cv2.putText(image, str(angle), 
                            tuple(np.multiply(elbow, [640, 480]).astype(int)), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                    )
                
                # Curl counter logic
                if angle > 160:
                    stage = "down"
                if angle < 30 and stage =='down':
                    stage="up"
                    counter +=1
                    # print(counter)
                    
                
                        
            except:
                cv2.putText(image, "Warning! No pose detected", (150,200), cv2.FONT_HERSHEY_SIMPLEX, 1, [0,0,255], 2, cv2.LINE_AA)
                pass
            
            # Render curl counter
            # Setup status box
            cv2.rectangle(image, (0,0), (200,73), (255,255,255), -1)
            
            # Rep data
            cv2.putText(image, 'count', (15,12), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,153,0), 1, cv2.LINE_AA)
            cv2.putText(image, str(counter),
                        (10,60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)
            
            # Stage data
            cv2.putText(image, 'STAGE', (80,12), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,153,0), 1, cv2.LINE_AA)
            cv2.putText(image, stage, 
                        (70,60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)
            
                    
            
            # Render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                    mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                    )               
            
            resized = cv2.resize(image, (1200,850), interpolation = cv2.INTER_AREA)
            cv2.imshow('count curls', resized)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()
    end=time.time()
    # print("-----------------------"+str(id)+"--------------------")
    df=pd.read_csv('users.csv')
    id=int(id)
    id=id-1
    df.loc[id,'time']=df.loc[id,'time']+int((end-start)/60)
    df.loc[id,'calorie_burnt']=df.loc[id,'calorie_burnt']+counter*0.5 # for 1count 0.5cal burn
    df.to_csv('users.csv',index=False)
    # csv_writer=csv.writer(open('users.csv','a',newline=""))
    id1=id+1
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
        df1.loc[row1,'calorie']=df1.loc[row1,'calorie']+counter*0.5
        df1.to_csv('daily.csv',index=False)
    else:
        csv_writer=csv.writer(open('daily.csv','a',newline=""))
        lis=[id1,df.loc[id,'name'],date.today(),int((end-start)/60),counter*0.5]
        csv_writer.writerow(lis)
    
    


