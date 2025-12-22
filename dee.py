import pyautogui
from pynput.keyboard import (
Key,
Controller as KeyboardController
)

# Initialize controllers
keyboard = KeyboardController()
mouse = MouseController()

# Screen size
SCREEN_W, SCREEN_H = pyautogui.size()

# Smoothing factor for cursor movement
SMOOTHING = 5
prev_x, prev_y = 0, 0


def move_cursor(hand_x, hand_y):
    """
    Move cursor based on normalized hand position (0 to 1)
    """
    global prev_x, prev_y

    x = int(hand_x * SCREEN_W)
    y = int(hand_y * SCREEN_H)

    # Smooth movement
    curr_x = prev_x + (x - prev_x) / SMOOTHING
    curr_y = prev_y + (y - prev_y) / SMOOTHING

    pyautogui.moveTo(curr_x, curr_y)
    prev_x, prev_y = curr_x, curr_y


def left_click():
    pyautogui.click()


def right_click():
    pyautogui.rightClick()


def scroll(up=True):
    pyautogui.scroll(300 if up else -300)


def volume_control(up=True):
    with keyboard.pressed(Key.media_volume_up if up else Key.media_volume_down):
        pass


def switch_tab(next_tab=True):
    keyboard.press(Key.ctrl)
    keyboard.press(Key.tab if next_tab else Key.shift)
    keyboard.release(Key.tab if next_tab else Key.shift)
    keyboard.release(Key.ctrl)


def perform_action(gesture, hand_pos):
    """
    gesture: string (e.g., 'open_palm', 'fist', 'peace')
    hand_pos: tuple (x, y) normalized between 0–1
    """

    x, y = hand_pos

    if gesture == "pointing":
        move_cursor(x, y)

    elif gesture == "pinch":
        left_click()

    elif gesture == "fist":
        right_click()

    elif gesture == "open_palm":
        scroll(up=True)

    elif gesture == "swipe_down":
        scroll(up=False)

    elif gesture == "thumbs_up":
        volume_control(up=True)

    elif gesture == "thumbs_down":
        volume_control(up=False)

    elif gesture == "peace":
        switch_tab(next_tab=True)

    else:
        pass  # No action