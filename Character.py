# Character.py
import numpy as np
from PIL import Image

class Character:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.position = np.array([width/2 - 30, height - 70, width/2 + 30, height - 10])
        self.walk_state = 0
        self.run_state = 0
        self.walk_speed = 5
        self.run_speed = 10
        self.direction = "right"
        self.is_running = False
        self.animation_speed = 0
        self.is_moving = False  # 움직임 상태 추가
        
    def move(self, command):
        move_speed = self.run_speed if self.is_running else self.walk_speed
        
        # 이동 상태 초기화
        self.is_moving = False
        
        if command['left_pressed']:
            self.is_moving = True
            self.direction = "left"
            self.position[0] = max(0, self.position[0] - move_speed)
            self.position[2] = self.position[0] + 60
            self.animation_speed += 1
            
            if self.is_running:
                self.run_state = (self.run_state + 1) % 8
            else:
                self.walk_state = (self.walk_state + 1) % 8
            
        elif command['right_pressed']:
            self.is_moving = True
            self.direction = "right"
            self.position[0] = min(self.width - 60, self.position[0] + move_speed)
            self.position[2] = self.position[0] + 60
            self.animation_speed += 1
            
            if self.is_running:
                self.run_state = (self.run_state + 1) % 8
            else:
                self.walk_state = (self.walk_state + 1) % 8
        else:
            self.walk_state = 0
            self.run_state = 0
            self.animation_speed = 0
            
    def set_running(self, is_running):
        self.is_running = is_running