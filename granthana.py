import math


def distance(p1, p2):
    """Calculate Euclidean distance between two points"""
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


def recognize_gesture(finger_states, landmarks=None, prev_landmarks=None):
    """
    Recognize hand gesture based on finger states and landmarks
    
    finger_states: [thumb, index, middle, ring, pinky]
                   1 = up, 0 = down
    landmarks: dictionary of landmark positions (optional)
    prev_landmarks: previous frame landmarks for swipe detection (optional)
    
    Returns: gesture name (string)
    """
    
    if not finger_states or len(finger_states) != 5:
        return "none"
    
    total = sum(finger_states)
    thumb, index, middle, ring, pinky = finger_states
    
    # -------- FIST (all down) --------
    if total == 0:
        return "fist"
    
    # -------- THUMBS UP (only thumb) --------
    if finger_states == [1, 0, 0, 0, 0]:
        return "thumbs_up"
    
    # -------- POINTING (only index) --------
    if finger_states == [0, 1, 0, 0, 0]:
        return "pointing"
    
    # -------- PEACE (index + middle only) --------
    if index == 1 and middle == 1 and total == 2:
        return "peace"
    
    # -------- PINCH (thumb + index close together) --------
    if landmarks:
        thumb_tip = landmarks.get("thumb_tip")
        index_tip = landmarks.get("index_tip")
        
        if thumb_tip and index_tip:
            if distance(thumb_tip, index_tip) < 0.05:
                return "pinch"
    
    # -------- THREE FINGERS --------
    if total == 3:
        return "three"
    
    # -------- OPEN PALM (4 or 5 fingers up) --------
    if total >= 4:
        return "open_palm"
    
    # -------- SWIPE DETECTION --------
    if landmarks and prev_landmarks:
        curr_x = landmarks.get("index_tip", (0, 0))[0]
        prev_x = prev_landmarks.get("index_tip", (0, 0))[0]
        
        if curr_x - prev_x > 0.15:
            return "swipe_right"
        elif prev_x - curr_x > 0.15:
            return "swipe_left"
    
    return "unknown"


if __name__ == "__main__":
    # Test cases
    print("Testing gesture recognition:")
    print(f"[0,0,0,0,0] = {recognize_gesture([0,0,0,0,0])}")  # fist
    print(f"[1,0,0,0,0] = {recognize_gesture([1,0,0,0,0])}")  # thumbs_up
    print(f"[0,1,0,0,0] = {recognize_gesture([0,1,0,0,0])}")  # pointing
    print(f"[0,1,1,0,0] = {recognize_gesture([0,1,1,0,0])}")  # peace
    print(f"[1,1,1,1,1] = {recognize_gesture([1,1,1,1,1])}")  # open_palm


