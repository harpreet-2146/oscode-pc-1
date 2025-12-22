
import cv2
import mediapipe as mp


class HandDetector:
    def __init__(
        self,
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    ):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=static_image_mode,
            max_num_hands=max_num_hands,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )
        self.mp_draw = mp.solutions.drawing_utils

    def detect(self, frame, draw=True):
        """
        Detect hands in a frame.

        Returns:
            hands_data: list of dicts
                [
                    {
                        "handedness": "Left" or "Right",
                        "landmarks": [(x, y, z), ...]  # 21 points
                    }
                ]
        """
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(img_rgb)

        hands_data = []

        if results.multi_hand_landmarks and results.multi_handedness:
            for hand_landmarks, handedness in zip(
                results.multi_hand_landmarks,
                results.multi_handedness,
            ):
                landmarks = []
                for lm in hand_landmarks.landmark:
                    landmarks.append((lm.x, lm.y, lm.z))

                hand_info = {
                    "handedness": handedness.classification[0].label,
                    "landmarks": landmarks,
                }
                hands_data.append(hand_info)

                if draw:
                    self.mp_draw.draw_landmarks(
                        frame,
                        hand_landmarks,
                        self.mp_hands.HAND_CONNECTIONS,
                    )

        return hands_data


def main():
    cap = cv2.VideoCapture(0)
    detector = HandDetector()

    while True:
        success, frame = cap.read()
        if not success:
            break

        hands = detector.detect(frame)

        for hand in hands:
            print(hand["handedness"], hand["landmarks"])

        cv2.imshow("Hand Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
