"""
Gesture Control - Main Integration (preeti.py)
Connects: mayank.py, Ranjan.py, granthana.py, dee.py
"""

import cv2
import time

# Import team modules
from Ranjan import HandDetector
from granthana import recognize_gesture
from dee import perform_action, SCREEN_W, SCREEN_H

# Cooldowns
last_action_time = 0
ACTION_COOLDOWN = 0.7  # seconds between clicks

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

detector = HandDetector(detection_con=0.7, track_con=0.7)
prev_landmarks = None

print("=" * 50)
print("🖐️  GESTURE CONTROL SYSTEM")
print("=" * 50)
print("☝️  POINT (index)     → Move cursor")
print("✌️  PEACE (2 fingers) → Left click")
print("✊  FIST (0 fingers)  → Right click")
print("🖐️  PALM (5 fingers)  → Scroll up")
print("👍  THUMB only        → Volume up")
print("=" * 50)
print("Press 'q' to quit")
print("=" * 50)

while True:
    success, frame = cap.read()
    if not success:
        print("❌ Camera error")
        break
    
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    
    # Detect hand and fingers
    frame = detector.find_hands(frame, draw=True)
    fingers = detector.get_finger_status()
    landmarks = detector.get_landmark_positions()
    
    gesture = "none"
    finger_count = 0
    
    if fingers and landmarks:
        finger_count = sum(fingers)
        gesture = recognize_gesture(fingers, landmarks, prev_landmarks)
        
        current_time = time.time()
        
        # Actions that need cooldown
        if gesture in ["peace", "fist", "thumbs_up", "pinch", "swipe_left", "swipe_right"]:
            if current_time - last_action_time > ACTION_COOLDOWN:
                perform_action(gesture, landmarks.get("index_tip"))
                last_action_time = current_time
                print(f"🎯 {gesture.upper()}")
        
        # Actions without cooldown (continuous)
        elif gesture in ["pointing", "open_palm"]:
            perform_action(gesture, landmarks.get("index_tip"))
        
        prev_landmarks = landmarks
        
        # Draw circle on index finger
        idx_tip = landmarks.get("index_tip")
        if idx_tip:
            cx, cy = int(idx_tip[0] * w), int(idx_tip[1] * h)
            cv2.circle(frame, (cx, cy), 15, (0, 255, 0), -1)
    
    # ===== UI =====
    cv2.rectangle(frame, (0, 0), (w, 90), (0, 0, 0), -1)
    
    cv2.putText(frame, f"Gesture: {gesture}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
    
    if fingers:
        cv2.putText(frame, f"Fingers: {fingers} ({finger_count} up)", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 2)
    
    status = "TRACKING" if fingers else "NO HAND"
    color = (0, 255, 0) if fingers else (0, 0, 255)
    cv2.putText(frame, status, (w - 150, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    
    cv2.imshow("Gesture Control", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("\n👋 Bye!")
