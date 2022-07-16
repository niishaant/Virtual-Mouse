# 6 EASY STEPS TO CREATE A VIRTUAL MOUSE
# step1 = Opening Camera
import cv2
import mediapipe as mp
import pyautogui

# HAND DETECTION STEP
cap = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils

screen_width, screen_height = pyautogui.size()

index_y = 0

while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)  # Flip The Camera
    frame_height, frame_width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks

    # our hand contains 21 points over thumbs , index , middle , ring and pinky fingers
    if hands:
        for hand in hands:  # iteration step
            drawing_utils.draw_landmarks(frame, hand)

            # STEP - 3 = Iterating landmarks on our hand
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)
                print(x, y)

                if id == 8:  # checking for index finger
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))

                    # converting your frame into laptop size frame ( screen factor or whatever you like to say)
                    index_x = screen_width / frame_width * x
                    index_y = screen_height / frame_height * y

                    # Step4 = Move your finger here n there to check if your cursor moves or not
                    pyautogui.moveTo(index_x, index_y)
                    # after executing above line it'll only be limited to some space not
                    # on your whole laptop screen because of the frames

                if id == 4:  # intersection of thumb with index finger results in click of our virtual mouse
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    thumb_x = screen_width / frame_width * x
                    thumb_y = screen_height / frame_height * y

                    print('outside', abs(index_y - thumb_y))
                    if abs(index_y - thumb_y) < 30:
                        pyautogui.click()
                        pyautogui.sleep(2)

    cv2.imshow('Virtual Mouse', frame)
    cv2.waitKey(1)
