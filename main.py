import cv2
import mediapipe as mp
import numpy as np

# Camera setup
wCam, hCam = 1200, 400
video = cv2.VideoCapture(1, cv2.CAP_DSHOW)
video.set(cv2.CAP_PROP_FRAME_WIDTH, wCam)
video.set(cv2.CAP_PROP_FRAME_HEIGHT, hCam)

if not video.isOpened():
    print("Error: cannot open camera.")
    exit()

# MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

# Canvas
canvas = None
prev_x, prev_y = 0, 0
brush_thickness = 5
eraser_thickness = 100

# Colors/functions (3 colors + eraser)
items = [
    {"label": "Yellow", "color": (0, 255, 255)},
    {"label": "Green", "color": (0, 255, 0)},
    {"label": "Red", "color": (0, 0, 255)},
    {"label": "Eraser", "color": (50, 50, 50)}
]
current_index = 0
current_label = items[current_index]["label"]
current_color = items[current_index]["color"]
last_gesture = None

def count_fingers(hand_landmarks):
    fingers = []
    if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
        fingers.append(1)
    else:
        fingers.append(0)
    tips = [8, 12, 16, 20]
    for tip in tips:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)
    return fingers

def draw_top_panel(img, finger_count, items, current_index):
    h, w, _ = img.shape
    panel_h = 60
    cv2.rectangle(img, (0, 0), (w, panel_h), (30, 30, 30), -1)  # background

    block_w = 100
    gap = 15
    x_start = 20

    for i, item in enumerate(items):
        x = x_start + i*(block_w + gap)
        y = 10
        # Highlight current selection
        if i == current_index:
            cv2.rectangle(img, (x-5, y-5), (x+block_w+5, y+block_w-5), (200, 200, 200), -1)
        # Draw color block
        cv2.rectangle(img, (x, y), (x+block_w, y+block_w-10), item["color"], -1)
        # Label text
        text_color = (255,255,255) if item["label"]!="Eraser" else (0,0,0)
        cv2.putText(img, item["label"], (x+5, y+block_w+15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 1)
    
    # Finger count
    cv2.putText(img, f'Fingers: {finger_count}', (w-180, 35),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

while True:
    success, img = video.read()
    if not success:
        print("Error capturing frame")
        break

    img = cv2.flip(img, 1)
    if canvas is None:
        canvas = np.zeros_like(img)

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    finger_count_display = 0

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            h, w, _ = img.shape
            cx = int(hand_landmarks.landmark[8].x * w)
            cy = int(hand_landmarks.landmark[8].y * h)

            fingers = count_fingers(hand_landmarks)
            finger_count = sum(fingers)
            finger_count_display = finger_count

            gesture_label = None
            # Map gestures
            if finger_count == 1 and fingers[1]==1:
                gesture_label = "Draw"
            elif finger_count == 2:
                gesture_label = "Yellow"
            elif finger_count == 3:
                gesture_label = "Green"
            elif finger_count == 4:
                gesture_label = "Red"
            elif finger_count == 5:
                gesture_label = "Eraser"

            # Update selection only when gesture changes
            if gesture_label and gesture_label != last_gesture:
                last_gesture = gesture_label
                for idx, item in enumerate(items):
                    if item["label"] == gesture_label:
                        current_index = idx
                        current_label = item["label"]
                        current_color = item["color"]

            # Draw with 1 finger
            if finger_count == 1 and fingers[1]==1:
                if prev_x==0 and prev_y==0:
                    prev_x, prev_y = cx, cy
                cv2.line(canvas, (prev_x, prev_y), (cx, cy),
                         current_color, brush_thickness)
                prev_x, prev_y = cx, cy
            # Eraser
            elif finger_count==5:
                cv2.circle(canvas, (cx, cy), eraser_thickness, (0,0,0), -1)
                prev_x, prev_y=0,0
            else:
                prev_x, prev_y=0,0

    # Combine canvas
    gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, inv = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY_INV)
    inv = cv2.cvtColor(inv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, inv)
    img = cv2.bitwise_or(img, canvas)

    # Draw HUD panel
    draw_top_panel(img, finger_count_display, items, current_index)

    cv2.imshow("Air Draw - HUD Panel", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()