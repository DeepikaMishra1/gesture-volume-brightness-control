import cv2
import mediapipe as mp
import math

from pycaw.pycaw import AudioUtilities


# ==========================================
# 1. WINDOWS VOLUME SETUP
# ==========================================

devices = AudioUtilities.GetSpeakers()

# New Pycaw version
volume = devices.EndpointVolume

min_volume, max_volume, _ = volume.GetVolumeRange()


# ==========================================
# 2. MEDIAPIPE HAND DETECTION
# ==========================================

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)


# ==========================================
# 3. CAMERA
# ==========================================

cap = cv2.VideoCapture(0, cv2.CAP_MSMF)

if not cap.isOpened():
    print("Camera not detected")
    exit()

print("Camera connected successfully!")
print("Hand Gesture Volume Control Started")
print("Press Q to exit")


# ==========================================
# 4. MAIN LOOP
# ==========================================

while True:

    success, frame = cap.read()

    if not success:
        print("Could not read camera")
        break

    # Mirror camera
    frame = cv2.flip(frame, 1)

    # Convert BGR to RGB
    rgb_frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    # Detect hand
    results = hands.process(rgb_frame)


    # ======================================
    # 5. IF HAND IS DETECTED
    # ======================================

    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            # Draw hand landmarks
            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )


            # ==================================
            # THUMB TIP = LANDMARK 4
            # INDEX TIP = LANDMARK 8
            # ==================================

            thumb = hand_landmarks.landmark[4]
            index = hand_landmarks.landmark[8]


            h, w, c = frame.shape


            # Thumb coordinates
            thumb_x = int(thumb.x * w)
            thumb_y = int(thumb.y * h)


            # Index finger coordinates
            index_x = int(index.x * w)
            index_y = int(index.y * h)


            # ==================================
            # DRAW CIRCLES
            # ==================================

            cv2.circle(
                frame,
                (thumb_x, thumb_y),
                10,
                (255, 0, 255),
                cv2.FILLED
            )

            cv2.circle(
                frame,
                (index_x, index_y),
                10,
                (255, 0, 255),
                cv2.FILLED
            )


            # ==================================
            # DRAW LINE
            # ==================================

            cv2.line(
                frame,
                (thumb_x, thumb_y),
                (index_x, index_y),
                (255, 0, 255),
                3
            )


            # ==================================
            # CALCULATE DISTANCE
            # ==================================

            distance = math.hypot(
                index_x - thumb_x,
                index_y - thumb_y
            )


            # ==================================
            # DISTANCE → VOLUME
            # ==================================

            volume_percent = (distance - 30) * 100 / 170

            # Keep volume between 0 and 100
            volume_percent = max(
                0,
                min(100, volume_percent)
            )


            # ==================================
            # VOLUME PERCENT → WINDOWS LEVEL
            # ==================================

            volume.SetMasterVolumeLevelScalar(
    volume_percent / 100,
    None
)
            


            # ==================================
            # DISPLAY VOLUME
            # ==================================

            cv2.putText(
                frame,
                f"Volume: {int(volume_percent)}%",
                (30, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.2,
                (0, 255, 0),
                3
            )


            # ==================================
            # DISPLAY DISTANCE
            # ==================================

            cv2.putText(
                frame,
                f"Distance: {int(distance)}",
                (30, 100),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 255),
                2
            )


    # ======================================
    # 6. SHOW CAMERA WINDOW
    # ======================================

    cv2.imshow(
        "Hand Gesture Volume Control",
        frame
    )


    # ======================================
    # 7. PRESS Q TO EXIT
    # ======================================

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# ==========================================
# 8. CLOSE EVERYTHING
# ==========================================

cap.release()
cv2.destroyAllWindows()

