import cv2
import mediapipe as mp


class HandDetector:
    def __init__(self, detection_con=0.7, track_con=0.7):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=detection_con,
            min_tracking_confidence=track_con
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.results = None
        self.handedness = "Right"

    def find_hands(self, img, draw=True):
        """Processes the image and detects hands"""
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)

        if self.results.multi_hand_landmarks:
            if draw:
                for hand_lms in self.results.multi_hand_landmarks:
                    self.mp_draw.draw_landmarks(img, hand_lms, self.mp_hands.HAND_CONNECTIONS)
            
            # Get handedness
            if self.results.multi_handedness:
                self.handedness = self.results.multi_handedness[0].classification[0].label
        
        return img

    def get_finger_status(self, img=None):
        """
        Returns a list: [Thumb, Index, Middle, Ring, Pinky]
        1 = Finger is UP, 0 = Finger is DOWN
        """
        fingers = []
        tips = [4, 8, 12, 16, 20]
        
        if not self.results or not self.results.multi_hand_landmarks:
            return []
        
        landmarks = self.results.multi_hand_landmarks[0].landmark
        
        # Thumb - check x direction (accounts for left/right hand)
        if self.handedness == "Right":
            if landmarks[tips[0]].x < landmarks[tips[0] - 1].x:
                fingers.append(1)
            else:
                fingers.append(0)
        else:
            if landmarks[tips[0]].x > landmarks[tips[0] - 1].x:
                fingers.append(1)
            else:
                fingers.append(0)
        
        # Other 4 fingers - tip above pip joint means finger is up
        for i in range(1, 5):
            if landmarks[tips[i]].y < landmarks[tips[i] - 2].y:
                fingers.append(1)
            else:
                fingers.append(0)
        
        return fingers

    def get_landmark_positions(self):
        """Returns dictionary of key landmark positions"""
        if not self.results or not self.results.multi_hand_landmarks:
            return None
        
        landmarks = self.results.multi_hand_landmarks[0].landmark
        
        return {
            "thumb_tip": (landmarks[4].x, landmarks[4].y),
            "index_tip": (landmarks[8].x, landmarks[8].y),
            "middle_tip": (landmarks[12].x, landmarks[12].y),
            "ring_tip": (landmarks[16].x, landmarks[16].y),
            "pinky_tip": (landmarks[20].x, landmarks[20].y),
            "wrist": (landmarks[0].x, landmarks[0].y)
        }


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    detector = HandDetector()

    while True:
        success, img = cap.read()
        if not success:
            break
        
        img = cv2.flip(img, 1)
        img = detector.find_hands(img)
        fingers = detector.get_finger_status()
        
        if fingers:
            cv2.putText(img, f"Fingers: {fingers} ({sum(fingers)} up)", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        cv2.imshow("Finger Detection", img)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
