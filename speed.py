import cv2
import mediapipe as mp
import time
import math
# from app import id

# Function to calculate distance between two points (x1, y1) and (x2, y2)
def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# Initialize MediaPipe Hand model
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Set up MediaPipe Drawing utilities
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


def pixels_to_meters(pixels):
    # Example conversion factor (adjust as needed based on your scenario)
    pixels_per_meter = 100  # 100 pixels per meter
    return pixels / pixels_per_meter

def speed1():
    # Initialize variables
    previous_time = 0
    previous_x = 0
    previous_y = 0
        # Capture video from webcam
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        # Flip the image horizontally for a later selfie-view display
        image = cv2.flip(image, 1)

        # Convert the BGR image to RGB
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Process the image with MediaPipe Hands
        results = hands.process(rgb_image)
        speed = 0


        # Draw landmarks on the image if hand(s) detected
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
              if results.multi_hand_landmarks and len(results.multi_hand_landmarks) == 1:
                # Extract x, y coordinates of the wrist
                global x
                x = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x * image.shape[1]
                y = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y * image.shape[0]
                
                # Calculate distance moved and speed
                if previous_time != 0:
                    current_time = time.time()
                    time_difference = current_time - previous_time
                    if time_difference != 0:
                        distance = calculate_distance(previous_x, previous_y, x, y)
                        distance = pixels_to_meters(distance)
                        speed = distance / time_difference
                        speed = round(speed,1)
                        # print("Speed:", speed, "pixels per second")
                    
                # Store current x, y coordinates and time for next iteration
                previous_x = x
                previous_y = y
                previous_time = time.time()

                # Draw a circle at the detected point
                cv2.circle(image, (int(x), int(y)), 10, (0, 255, 0), -1)
        cv2.rectangle(image, (0,0), (200,73), (255,255,255), -1)
                    
                    # Rep data
        cv2.putText(image, 'speed', (15,18), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,153,0), 1, cv2.LINE_AA)
        cv2.putText(image, str(speed)+" m/s",
                                (10,60), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)

        # Display the image with landmarks
        resized = cv2.resize(image, (1200,850), interpolation = cv2.INTER_AREA)

        cv2.imshow('MediaPipe Hands', resized)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()