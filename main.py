import cv2
import mediapipe as mp
import pyautogui
from google.protobuf.json_format import MessageToDict
import keyboard

# Initialize Mediapipe Hand model
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Initialize PyAutoGUI
pyautogui.FAILSAFE = False

deltaLeft = 0.4
deltaRight = 0.2

# Initialize video capture
cap = cv2.VideoCapture(0)

with mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            break

        # Convert the image to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Process the image with Mediapipe
        results = hands.process(image_rgb)

        # Check if hand landmarks are detected
        if results.multi_hand_landmarks:
            # for hand_landmarks in results.multi_hand_landmarks:
            for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                # Get the x-coordinate of the thumb and little finger
                thumb_y = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y
                pinky_y = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y

                lbl = results.multi_handedness[idx].classification[0].label

                # print(lbl + " hand detected")
                # print(thumb_y, pinky_y)

                # Determine the hand tilt direction
                if lbl == 'Right':
                    if thumb_y > pinky_y + deltaLeft:
                        # Press right key
                        print('moving left')
                        keyboard.press('a')
                    elif pinky_y > thumb_y + deltaRight:
                        # Press left key
                        keyboard.press('d')
                        print('moving right')
                    else:
                        keyboard.release('a')
                        keyboard.release('d')
                        print('not moving')
                elif lbl == 'Left':
                    if thumb_y > pinky_y + deltaLeft:
                        # Press left key

                        keyboard.press('a')
                        print('moving left')
                    elif pinky_y > thumb_y + deltaRight:
                        # Press right key
                        keyboard.press('d')
                        print('moving right')
                    else:
                        keyboard.release('a')
                        keyboard.release('d')
                        print('not moving')

            # # Draw hand landmarks on the image
            # mp_drawing.draw_landmarks(
            #     image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Display the image
        cv2.imshow('Hand Tilt Detection', image)

        # Exit loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release the video capture and close all windows
# Draw hand landmarks on the image
if results.multi_hand_landmarks:
    for hand_landmarks in results.multi_hand_landmarks:
        mp_drawing.draw_landmarks(
            image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

# Display the image
# cv2.imshow('Hand Tilt Detection', image)

# Exit loop if 'q' is pressed
if cv2.waitKey(1) & 0xFF == ord('q'):
    exit()

cap.release()
cv2.destroyAllWindows()
