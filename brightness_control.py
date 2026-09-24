import cv2
import mediapipe as mp
import math
import screen_brightness_control as sbc
from pycaw.pycaw import AudioUtilities


# =========================
# VOLUME SETUP
# =========================

devices = AudioUtilities.GetSpeakers()
volume = devices.EndpointVolume


# =========================
# BRIGHTNESS SETUP
# =========================

monitors = sbc.list_monitors()

print("Detected monitor:", monitors)

if not monitors:
    print("No monitor detected for brightness control.")
    exit()

monitor = monitors[0]

print("Using monitor:", monitor)
print("Current brightness:", sbc.get_brightness(display=monitor))


# =========================
# MEDIAPIPE
# =========================

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)


# =========================
# CAMERA
# =========================

cap = cv2.VideoCapture(0, cv2.CAP_MSMF)

if not cap.isOpened():
    print("Camera not detected")
    exit()

print("Camera connected successfully!")
print("Hand Gesture Volume + Brightness Control Started")
print("Press Q to exit")


last_level = -1


# =========================
# MAIN LOOP
# =========================

while True:

    success, frame = cap.read()

    if not success:
        print("Could not read camera")
        break

    frame = cv2.flip(frame, 1)

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb_frame)


    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )


            # Thumb = 4
            # Index finger = 8

            thumb = hand_landmarks.landmark[4]
            index = hand_landmarks.landmark[8]

            h, w, c = frame.shape

            thumb_x = int(thumb.x * w)
            thumb_y = int(thumb.y * h)

            index_x = int(index.x * w)
            index_y = int(index.y * h)


            # Draw points

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


            # Distance

            distance = math.hypot(
                index_x - thumb_x,
                index_y - thumb_y
            )


            cv2.line(
                frame,
                (thumb_x, thumb_y),
                (index_x, index_y),
                (255, 0, 255),
                3
            )


            # =========================
            # DISTANCE → PERCENTAGE
            # =========================

            level = int(
                max(
                    0,
                    min(
                        100,
                        (distance - 30) * 100 / 170
                    )
                )
            )


            # =========================
            # VOLUME
            # =========================

            volume.SetMasterVolumeLevelScalar(
                level / 100,
                None
            )


            # =========================
            # BRIGHTNESS
            # =========================

            if level != last_level:

                try:

                    sbc.set_brightness(
                        level,
                        display=monitor
                    )

                    print(
                        f"Volume: {level}% | Brightness: {level}%"
                    )

                    last_level = level

                except Exception as e:

                    print(
                        "Brightness error:",
                        e
                    )


            # =========================
            # TEXT
            # =========================

            cv2.putText(
                frame,
                f"Volume: {level}%",
                (30, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.1,
                (0, 255, 0),
                3
            )

            cv2.putText(
                frame,
                f"Brightness: {level}%",
                (30, 105),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0,
                (0, 255, 255),
                3
            )

            cv2.putText(
                frame,
                f"Distance: {int(distance)}",
                (30, 145),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 255),
                2
            )


    cv2.imshow(
        "Hand Gesture Volume + Brightness Control",
        frame
    )


    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# =========================
# CLOSE
# =========================

cap.release()
cv2.destroyAllWindows()
hands.close()

print("Program stopped.")

