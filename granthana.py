import math

def distance(p1, p2):
    """Calculate Euclidean distance between two points"""
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


def recognize_gesture(finger_states, landmarks=None, prev_landmarks=None):
    """
    Recognize hand gesture based on finger states and landmarks
    
    finger_states: [thumb, index, middle, ring, pinky]
                   1 = open, 0 = closed
    landmarks: dictionary of landmark positions
    prev_landmarks: previous frame landmarks (for swipe detection)
    
    Returns: gesture name (string)
    """

    thumb, index, middle, ring, pinky = finger_states

    # -------- Static Gestures --------
    if finger_states == [0, 0, 0, 0, 0]:
        return "Fist"

    if finger_states == [1, 1, 1, 1, 1]:
        return "Open Palm"

    if finger_states == [0, 1, 1, 0, 0]:
        return "Peace Sign"

    if finger_states == [0, 1, 0, 0, 0]:
        return "Pointing"

    if finger_states == [1, 0, 0, 0, 0]:
        return "Thumbs Up"

    # -------- Pinch (Thumb + Index close) --------
    if landmarks:
        thumb_tip = landmarks.get("thumb_tip")
        index_tip = landmarks.get("index_tip")

        if thumb_tip and index_tip:
            if distance(thumb_tip, index_tip) < 0.05:
                return "Pinch"

    # -------- Swipe Detection --------
    if landmarks and prev_landmarks:
        curr_x = landmarks["index_tip"][0]
        prev_x = prev_landmarks["index_tip"][0]

        if curr_x - prev_x > 0.1:
            return "Swipe Right"
        elif prev_x - curr_x > 0.1:
            return "Swipe Left"

    return "Unknown Gesture"

