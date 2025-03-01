#!/usr/bin/env python3

import pyautogui

class GestureManager:
    def __init__(self):
        self.screen_width, self.screen_height = pyautogui.size()
        self.hand_Landmarks = None
        self.prev_hand = None
        self.right_clicked = False
        self.left_clicked = False
        self.double_clicked = False
        self.dragging = False
        
        self.little_finger_down = None
        self.little_finger_up = None
        self.index_finger_down = None
        self.index_finger_up = None
        self.middle_finger_down = None
        self.middle_finger_up = None
        self.ring_finger_down = None
        self.ring_finger_up = None
        self.thumb_finger_down = None
        self.thumb_finger_up = None
        self.all_fingers_down = None
        self.all_fingers_up = None
        self.index_finger_within_thumb_finger = None
        self.middle_finger_within_thumb_finger = None
        self.little_finger_within_thumb_finger = None
        self.ring_finger_within_thumb_finger = None
    
    def update_fingers_status(self):
        self.little_finger_down = self.hand_Landmarks.landmark[20].y > self.hand_Landmarks.landmark[17].y
        self.little_finger_up = self.hand_Landmarks.landmark[20].y < self.hand_Landmarks.landmark[17].y
        self.index_finger_down = self.hand_Landmarks.landmark[8].y > self.hand_Landmarks.landmark[5].y
        self.index_finger_up = self.hand_Landmarks.landmark[8].y < self.hand_Landmarks.landmark[5].y
        self.middle_finger_down = self.hand_Landmarks.landmark[12].y > self.hand_Landmarks.landmark[9].y
        self.middle_finger_up = self.hand_Landmarks.landmark[12].y < self.hand_Landmarks.landmark[9].y
        self.ring_finger_down = self.hand_Landmarks.landmark[16].y > self.hand_Landmarks.landmark[13].y
        self.ring_finger_up = self.hand_Landmarks.landmark[16].y < self.hand_Landmarks.landmark[13].y
        self.thumb_finger_down = self.hand_Landmarks.landmark[4].y > self.hand_Landmarks.landmark[2].y
        self.thumb_finger_up = self.hand_Landmarks.landmark[4].y < self.hand_Landmarks.landmark[2].y

        self.all_fingers_down = self.index_finger_down and self.middle_finger_down and self.ring_finger_down and self.little_finger_down
        self.all_fingers_up = self.index_finger_up and self.middle_finger_up and self.ring_finger_up and self.little_finger_up
        self.index_finger_within_thumb_finger = self.hand_Landmarks.landmark[8].y > self.hand_Landmarks.landmark[4].y and self.hand_Landmarks.landmark[8].y < self.hand_Landmarks.landmark[2].y
        self.middle_finger_within_thumb_finger = self.hand_Landmarks.landmark[12].y > self.hand_Landmarks.landmark[4].y and self.hand_Landmarks.landmark[12].y < self.hand_Landmarks.landmark[2].y
        self.little_finger_within_thumb_finger = self.hand_Landmarks.landmark[20].y > self.hand_Landmarks.landmark[4].y and self.hand_Landmarks.landmark[20].y < self.hand_Landmarks.landmark[2].y
        self.ring_finger_within_thumb_finger = self.hand_Landmarks.landmark[16].y > self.hand_Landmarks.landmark[4].y and self.hand_Landmarks.landmark[16].y < self.hand_Landmarks.landmark[2].y
    
    def get_position(self, hand_x_position, hand_y_position):
        old_x, old_y = pyautogui.position()
        current_x = int(hand_x_position * self.screen_width)
        current_y = int(hand_y_position * self.screen_height)
        
        ratio = 1
        if self.prev_hand is None:
            self.prev_hand = (current_x, current_y)
        
        delta_x = current_x - self.prev_hand[0]
        delta_y = current_y - self.prev_hand[1]
        self.prev_hand = (current_x, current_y)
        
        current_x, current_y = old_x + delta_x * ratio, old_y + delta_y * ratio
        threshold = 5
        
        current_x = max(threshold, min(current_x, self.screen_width - threshold))
        current_y = max(threshold, min(current_y, self.screen_height - threshold))
        
        return (current_x, current_y)
    
    def cursor_moving(self):
        point = 9
        current_x, current_y = self.hand_Landmarks.landmark[point].x, self.hand_Landmarks.landmark[point].y
        x, y = self.get_position(current_x, current_y)
        
        cursor_freezed = self.all_fingers_up and self.thumb_finger_down
        if not cursor_freezed:
            pyautogui.moveTo(x, y, duration=0)
    
    def detect_scrolling(self):
        if self.little_finger_up and self.index_finger_down and self.middle_finger_down and self.ring_finger_down:
            pyautogui.scroll(120)
            print("Scrolling UP")
        if self.index_finger_up and self.middle_finger_down and self.ring_finger_down and self.little_finger_down:
            pyautogui.scroll(-120)
            print("Scrolling DOWN")
    
    def detect_zooming(self):
        zooming = self.index_finger_up and self.middle_finger_up and self.ring_finger_down and self.little_finger_down
        window = 0.05
        index_touches_middle = abs(self.hand_Landmarks.landmark[8].x - self.hand_Landmarks.landmark[12].x) <= window
        
        if zooming and index_touches_middle:
            pyautogui.keyDown('ctrl')
            pyautogui.scroll(-50)
            pyautogui.keyUp('ctrl')
            print("Zooming Out")
        elif zooming and not index_touches_middle:
            pyautogui.keyDown('ctrl')
            pyautogui.scroll(50)
            pyautogui.keyUp('ctrl')
            print("Zooming In")
