import cv2
import mediapipe as mp
import time
import datetime
import matplotlib.pyplot as plt
import math
# from celluloid import Camera
from scipy import spatial
# import pyshine as ps
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def detectPose(image, pose, display=True):
 
    output_image = image.copy()
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(imageRGB) 
    height, width, _ = image.shape
    landmarks = []
    if results.pose_landmarks:

        mp_drawing.draw_landmarks(output_image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                         mp_drawing.DrawingSpec(color = (0,0,255), thickness = 5, circle_radius = 2),
                         mp_drawing.DrawingSpec(color = (0,255,0),thickness = 5, circle_radius = 2)
                         )
        for landmark in results.pose_landmarks.landmark:
            
            landmarks.append((int(landmark.x * width), int(landmark.y * height),
                                  (landmark.z * width)))
    if display:
        plt.figure(figsize=[22,22])
        plt.subplot(121);plt.imshow(image[:,:,::-1]);plt.title("Original Image");plt.axis('off');
        plt.subplot(122);plt.imshow(output_image[:,:,::-1]);plt.title("Output Image");plt.axis('off');

        mp_drawing.plot_landmarks(results.pose_world_landmarks, mp_pose.POSE_CONNECTIONS)

    else:
        return output_image, landmarks