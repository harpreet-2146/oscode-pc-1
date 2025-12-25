# ✋ Gesture Control System

Control your laptop using hand gestures through your webcam. Built with OpenCV and MediaPipe.

**OSCode Project Cycle 1**

---

## 🎯 What It Does

Use your hand gestures to:
- Move the cursor
- Click (left & right)
- Scroll
- Control volume
- Switch tabs

No mouse needed — just your hand in front of the camera.

---

## 🖐️ Gestures

| Gesture | How To Do It | Action |
|---------|--------------|--------|
| ☝️ **Point** | Only index finger up | Move cursor |
| ✌️ **Peace** | Index + middle finger up | Left click |
| ✊ **Fist** | All fingers closed | Right click |
| 🖐️ **Open Palm** | All 5 fingers up | Scroll up |
| 👍 **Thumbs Up** | Only thumb up | Volume up |
| 🤏 **Pinch** | Thumb + index touching | Left click |
| 👋 **Swipe** | Move hand left/right quickly | Switch tabs |

---

## 🛠️ How It Works

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Webcam    │ ──▶ │   Detect    │ ──▶ │  Recognize  │ ──▶ │   Perform   │
│   Capture   │     │   Fingers   │     │   Gesture   │     │   Action    │
│ (mayank.py) │     │ (Ranjan.py) │     │(granthana.py│     │  (dee.py)   │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
```

1. **Camera captures your hand** → MediaPipe detects 21 landmark points on your hand
2. **Finger detection** → Checks which fingers are up or down based on landmark positions
3. **Gesture recognition** → Matches finger pattern to a known gesture (fist, peace, etc.)
4. **Action execution** → Triggers the corresponding laptop action (click, scroll, etc.)

---

## 📁 Project Structure

```
gesture-control/
├── mayank.py        # Hand detection using MediaPipe
├── Ranjan.py        # Finger state detection (up/down)
├── granthana.py     # Gesture recognition logic
├── dee.py           # System control actions
├── preeti.py        # Main integration file
└── requirements.txt # Dependencies
```

---

## 🚀 Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/gesture-control.git
cd gesture-control
```

### 2. Create virtual environment (Python 3.10 recommended)

```bash
py -3.10 -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run

```bash
python preeti.py
```

---

## 📋 Requirements

```
opencv-python==4.9.0.80
mediapipe==0.10.14
numpy==1.26.4
pyautogui==0.9.54
pynput==1.7.7
screeninfo==0.8.1
```

> **Note:** MediaPipe requires Python 3.10 or 3.11. It does not work on Python 3.12+

---

## 💡 Tips

- Keep your hand **clearly visible** in the camera frame
- Use in **good lighting** for better detection
- Keep a **plain background** if detection is inconsistent
- Move your hand **slowly** at first to get used to the controls
- Press `q` to quit the application

---

## 👥 Team

| Name | GitHub | Role |
|------|--------|------|
| Harpreet | [@harpreet-2146](https://github.com/harpreet-2146) | Team Lead, Integration |
| Ranjan | [@ranjan0247](https://github.com/ranjan0247) | Finger Detection |
| Dee | [@thizisdee](https://github.com/thizisdee) | System Control |
| Granthana | [@granthana2006](https://github.com/granthana2006) | Gesture Recognition |
| Mayank | [@mayankbargarh1234-dev](https://github.com/mayankbargarh1234-dev) | Hand Detection |

---

## 🎥 Demo

Show your hand to the webcam:

1. **Point** with index finger → cursor follows your finger
2. Make **peace sign** → clicks where cursor is
3. Make a **fist** → right clicks
4. **Open palm** → scrolls the page
5. **Thumbs up** → increases volume

---

*Built during OSCode Project Cycle 1*
