import pyautogui
from pynput.keyboard import Key, Controller as KeyboardController

# Setup
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0

keyboard = KeyboardController()
SCREEN_W, SCREEN_H = pyautogui.size()

# Smoothing for cursor
smooth_x, smooth_y = SCREEN_W // 2, SCREEN_H // 2
SMOOTHING = 0.3


def move_cursor(hand_x, hand_y):
    """
    Move cursor based on hand position (0 to 1 normalized)
    """
    global smooth_x, smooth_y
    
    # Invert x for mirror effect
    target_x = int((1 - hand_x) * SCREEN_W)
    target_y = int(hand_y * SCREEN_H)
    
    # Smooth movement
    smooth_x = smooth_x + (target_x - smooth_x) * SMOOTHING
    smooth_y = smooth_y + (target_y - smooth_y) * SMOOTHING
    
    pyautogui.moveTo(int(smooth_x), int(smooth_y))


def left_click():
    """Perform left click"""
    pyautogui.click()


def right_click():
    """Perform right click"""
    pyautogui.rightClick()


def double_click():
    """Perform double click"""
    pyautogui.doubleClick()


def scroll(amount=20):
    """Scroll up (positive) or down (negative)"""
    pyautogui.scroll(amount)


def volume_up():
    """Increase volume"""
    pyautogui.press('volumeup')


def volume_down():
    """Decrease volume"""
    pyautogui.press('volumedown')


def switch_tab():
    """Switch to next tab (Alt+Tab)"""
    pyautogui.hotkey('alt', 'tab')


def close_window():
    """Close current window (Alt+F4)"""
    pyautogui.hotkey('alt', 'F4')


def play_pause():
    """Play/pause media"""
    pyautogui.press('playpause')


def perform_action(gesture, hand_pos=None):
    """
    Main function to perform action based on gesture
    
    gesture: string (e.g., 'pointing', 'fist', 'peace')
    hand_pos: tuple (x, y) normalized between 0-1
    """
    
    if gesture == "pointing" and hand_pos:
        move_cursor(hand_pos[0], hand_pos[1])
    
    elif gesture == "peace":
        left_click()
    
    elif gesture == "pinch":
        left_click()
    
    elif gesture == "fist":
        right_click()
    
    elif gesture == "open_palm":
        scroll(20)
    
    elif gesture == "thumbs_up":
        volume_up()
    
    elif gesture == "thumbs_down":
        volume_down()
    
    elif gesture == "swipe_right":
        switch_tab()
    
    elif gesture == "swipe_left":
        switch_tab()
    
    elif gesture == "three":
        play_pause()


if __name__ == "__main__":
    print("Testing system controls...")
    print("Moving cursor to center...")
    move_cursor(0.5, 0.5)
    print("Done!")

