# Hand Gesture Volume & Brightness Control 🖐️🔊💡

Computer Vision aur MediaPipe ka use karke bana ek Real-time Python application jo aapke haath ke gestures (Thumb aur Index Finger ke beech ki distance) se system ka **Volume** aur **Screen Brightness** control karta hai.

---

## ✨ Features
* **Real-time Hand Tracking**: MediaPipe Hands library ka upayog karta hai.
* **Volume Control**: Thumb aur Index Finger ki doori ke hisaab se Windows Volume adjust karta hai.
* **Brightness Control**: System monitor ki brightness ko realtime mai change karta hai.
* **Visual Overlay**: OpenCV window mai distance, volume percentage, aur brightness level show karta hai.

---

## 🛠️ Tech Stack & Dependencies
* **Python 3.x**
* **OpenCV (`cv2`)**: Webcam stream aur visual rendering ke liye.
* **MediaPipe**: Hand tracking aur landmarks detection ke liye.
* **Pycaw**: Windows Audio endpoints ko control karne ke liye.
* **Screen Brightness Control (`screen_brightness_control`)**: Screen brightness modify karne ke liye.

---

## 📥 Installation

1. Repository ko clone karein:
   ```bash
   git clone [https://github.com/YOUR-USERNAME/gesture-volume-brightness-control.git](https://github.com/YOUR-USERNAME/gesture-volume-brightness-control.git)
   cd gesture-volume-brightness-control
