import cv2
import mediapipe as mp
import time
import datetime
import matplotlib.pyplot as plt
import math
# from celluloid import Camera
# import pyshine as ps
from calc_angle import calculateAngle
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def classifyPose(landmarks, output_image, display=False):
    
    # Initialize the label of the pose. It is not known at this stage.
    label = 'Unknown Pose'
    color = (0, 0, 255)
    left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
    left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value]
    left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]    
    right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
    right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value]
    right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]
    left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
    left_knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]
    left_ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]            
    right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]            
    right_knee = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value]
    right_ankle = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value]              
                  
    angle1 = calculateAngle(right_shoulder, right_elbow, right_wrist)
   
    angle2 = calculateAngle(left_shoulder, left_elbow, left_wrist)
    
    angle3 = calculateAngle(right_elbow, right_shoulder, right_hip)
    
    angle4 = calculateAngle(left_elbow, left_shoulder, left_hip)
    
    angle5 = calculateAngle(right_shoulder, right_hip, right_knee)
    
    angle6 = calculateAngle(left_shoulder, left_hip, left_knee)
    
    angle7 = calculateAngle(right_hip, right_knee, right_ankle)
    
    angle8 = calculateAngle(left_hip, left_knee, left_ankle)
    

    if angle2 > 160 and angle2 < 195 and angle1 > 160 and angle1 < 195:

        if angle4 > 70 and angle4 < 110 and angle3 > 70 and angle3 < 110:

            if angle8 > 165 and angle8 < 195 or angle7 > 165 and angle7 < 195:
 

                if (angle8 > 80 and angle8 < 120) or (angle7 > 80 and angle7 < 120):

                    label = 'Warrior II Pose'             
  
 
            if (angle8 > 160 and angle8 < 195) and (angle7 > 160 and angle7 < 195):
 
                label = 'T Pose'
 

    if (angle8 > 165 and angle8 < 195) or (angle7 > 165 and angle7 < 195):

        if (angle7 > 25 and angle7 < 45) or (angle8 > 25 and angle8 < 45):
 
            label = 'Tree Pose'

    if label != 'Unknown Pose':

        color = (0, 0, 255)  

    cv2.putText(output_image, label, (400, 50),cv2.FONT_HERSHEY_PLAIN, 4, color, 4)
    cv2.rectangle(output_image,(0,0), (100,255), (255,255,255), -1)

    cv2.putText(output_image, 'ID', (10,14), cv2.FONT_HERSHEY_SIMPLEX, 0.6, [0,0,255], 2, cv2.LINE_AA)
    cv2.putText(output_image, str(1), (10,40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, [0,153,0], 2, cv2.LINE_AA)
    cv2.putText(output_image, str(2), (10,70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, [0,153,0], 2, cv2.LINE_AA)
    cv2.putText(output_image, str(3), (10,100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, [0,153,0], 2, cv2.LINE_AA)
    cv2.putText(output_image, str(4), (10,130), cv2.FONT_HERSHEY_SIMPLEX, 0.7, [0,153,0], 2, cv2.LINE_AA)
    cv2.putText(output_image, str(5), (10,160), cv2.FONT_HERSHEY_SIMPLEX, 0.7, [0,153,0], 2, cv2.LINE_AA)
    cv2.putText(output_image, str(6), (10,190), cv2.FONT_HERSHEY_SIMPLEX, 0.7, [0,153,0], 2, cv2.LINE_AA)
    cv2.putText(output_image, str(7), (10,220), cv2.FONT_HERSHEY_SIMPLEX, 0.7, [0,153,0], 2, cv2.LINE_AA)
    cv2.putText(output_image, str(8), (10,250), cv2.FONT_HERSHEY_SIMPLEX, 0.7, [0,153,0], 2, cv2.LINE_AA)

    cv2.putText(output_image, 'Angle', (40,12), cv2.FONT_HERSHEY_SIMPLEX, 0.6, [0,0,255], 2, cv2.LINE_AA)
    cv2.putText(output_image, str(int(angle1)), (40,40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, [0,153,0], 2, cv2.LINE_AA)
    cv2.putText(output_image, str(int(angle2)), (40,70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, [0,153,0], 2, cv2.LINE_AA)
    cv2.putText(output_image, str(int(angle3)), (40,100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, [0,153,0], 2, cv2.LINE_AA)
    cv2.putText(output_image, str(int(angle4)), (40,130), cv2.FONT_HERSHEY_SIMPLEX, 0.7, [0,153,0], 2, cv2.LINE_AA)
    cv2.putText(output_image, str(int(angle5)), (40,160), cv2.FONT_HERSHEY_SIMPLEX, 0.7, [0,153,0], 2, cv2.LINE_AA)
    cv2.putText(output_image, str(int(angle6)), (40,190), cv2.FONT_HERSHEY_SIMPLEX, 0.7, [0,153,0], 2, cv2.LINE_AA)
    cv2.putText(output_image, str(int(angle7)), (40,220), cv2.FONT_HERSHEY_SIMPLEX, 0.7, [0,153,0], 2, cv2.LINE_AA)
    cv2.putText(output_image, str(int(angle8)), (40,250), cv2.FONT_HERSHEY_SIMPLEX, 0.7, [0,153,0], 2, cv2.LINE_AA)

    if display:
    
        plt.figure(figsize=[10,10])
        plt.imshow(output_image[:,:,::-1]);plt.title("Output Image");plt.axis('off');
        
    else:

        return output_image, label