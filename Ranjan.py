import cv2
import mediapipe as mp

class HandDetector:
    def __init__(self, detection_con=0.7, track_con=0.5):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=detection_con,
            min_tracking_confidence=track_con
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.tip_ids = [4, 8, 12, 16, 20]  # Landmarks for fingertips

    def find_hands(self, img, draw=True):
        """Processes the image and returns landmarks."""
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)

        if self.results.multi_hand_landmarks and draw:
            for hand_lms in self.results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(img, hand_lms, self.mp_hands.HAND_CONNECTIONS)
        
        return img

    def get_finger_status(self, img):
        """
        Returns a list of booleans: [Thumb, Index, Middle, Ring, Pinky]
        True = Finger is UP, False = Finger is DOWN
        """
        fingers = []
        
        # Check if any hands were detected
        if self.results.multi_hand_landmarks:
            my_hand = self.results.multi_hand_landmarks[0]
            lm_list = []
            
            # Convert normalized coordinates to pixel values
            h, w, c = img.shape
            for id, lm in enumerate(my_hand.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append([id, cx, cy])

            # --- Logic for Fingers ---
            
            # 1. Thumb (Tip x < IP x) - Logic varies based on left/right hand
            # This assumes right hand facing camera. Swap logic for left.
            # Generally: Check if tip is to the 'outside' of the knuckle
            if lm_list[self.tip_ids[0]][1] > lm_list[self.tip_ids[0] - 1][1]:
                fingers.append(True)
            else:
                fingers.append(False)

            # 2. Four Fingers (Index, Middle, Ring, Pinky)
            # Logic: If Tip y < PIP Joint y (Tip is higher than the second knuckle)
            # Note: In OpenCV, Y coordinates increase downwards.
            for id in range(1, 5):
                if lm_list[self.tip_ids[id]][2] < lm_list[self.tip_ids[id] - 2][2]:
                    fingers.append(True)
                else:
                    fingers.append(False)
        
        return fingers

def main():
    cap = cv2.VideoCapture(0)
    detector = HandDetector()

    print("Press 'q' to quit...")

    while True:
        success, img = cap.read()
        if not success:
            break

        # 1. Find Hand
        img = detector.find_hands(img)
        
        # 2. Get Finger Status
        fingers_up = detector.get_finger_status(img)

        # 3. Display Result if hand is detected
        if fingers_up:
            # Count how many are True
            count = fingers_up.count(True)
            
            # Show the list on screen [T, F, F, F, F]
            status_text = f"Fingers: {fingers_up}"
            count_text = f"Count: {count}"

            cv2.putText(img, status_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            cv2.putText(img, count_text, (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)

        cv2.imshow("Hand Finger Counter", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()