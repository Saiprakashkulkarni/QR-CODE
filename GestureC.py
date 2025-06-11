import cv2
import mediapipe as mp
import pyautogui
import ctypes  # For hiding the cursor on Windows

# Screen positions for Accelerate and Brake (customize as needed)
ACCELERATE_POS = (950, 1100)
BRAKE_POS = (250, 1100)

# Setup webcam and Mediapipe
cap = cv2.VideoCapture(0)
hands = mp.solutions.hands.Hands(max_num_hands=1, min_detection_confidence=0.8)
draw = mp.solutions.drawing_utils

accelerate_clicked = False
brake_clicked = False

def fingers_up(hand_landmarks):
    finger_tips = [8, 12, 16, 20]
    fingers = []

    # Thumb
    if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Other fingers
    for tip in finger_tips:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)
    return fingers

# Hide mouse cursor (Windows only)
ctypes.windll.user32.ShowCursor(False)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            draw.draw_landmarks(frame, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)
            finger_status = fingers_up(hand_landmarks)
            total_fingers = sum(finger_status)

            # Accelerate logic
            if total_fingers == 5:
                if not accelerate_clicked:
                    pyautogui.mouseDown(*ACCELERATE_POS)
                    accelerate_clicked = True
                    print("Accelerating")
            else:
                if accelerate_clicked:
                    pyautogui.mouseUp(*ACCELERATE_POS)
                    accelerate_clicked = False

            # Brake logic
            if total_fingers == 0:
                if not brake_clicked:
                    pyautogui.mouseDown(*BRAKE_POS)
                    brake_clicked = True
                    print("Braking")
            else:
                if brake_clicked:
                    pyautogui.mouseUp(*BRAKE_POS)
                    brake_clicked = False

    else:
        # No hand detected — release both buttons
        if accelerate_clicked:
            pyautogui.mouseUp(*ACCELERATE_POS)
            accelerate_clicked = False
        if brake_clicked:
            pyautogui.mouseUp(*BRAKE_POS)
            brake_clicked = False

    # Display text feedback on screen
    if accelerate_clicked:
        cv2.putText(frame, "Accelerate", (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
    if brake_clicked:
        cv2.putText(frame, "Brake", (30, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

    cv2.imshow("Gesture Game Control", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        # Release actions and show cursor again
        pyautogui.mouseUp(*ACCELERATE_POS)
        pyautogui.mouseUp(*BRAKE_POS)
        ctypes.windll.user32.ShowCursor(True)
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
