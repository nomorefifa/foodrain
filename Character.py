# Character.py
import numpy as np
from PIL import Image

class Character:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.base_size = 60  # 기본 크기 설정
        self.current_size = self.base_size  # 현재 크기
        self.size_increment = 0.1  # 크기 증가율을 변수로 선언 (30%)
        self.max_level = 5  # 커질 수 있는 최대 레벨 설정
        self.position = np.array([width/2 - 30, height - 70, width/2 + 30, height - 10])
        self.walk_state = 0
        self.run_state = 0
        self.walk_speed = 5
        self.run_speed = 10
        self.direction = "right"
        self.is_running = False
        self.animation_speed = 0
        self.is_moving = False  # 움직임 상태 추가

    def resize(self, size_level):
        level = min(size_level, self.max_level)  # 최대 레벨 제한
        old_center = (self.position[0] + self.current_size/2)  # 이전 중심점 저장
        # 기존: self.current_size = self.base_size * size_level
        # size_increment 변수 사용
        self.current_size = self.base_size * (1 + (level - 1) * self.size_increment)  
        
        # 새로운 위치 계산 (중심점 기준으로)
        new_left = old_center - self.current_size/2
        new_left = max(0, min(new_left, self.width - self.current_size))  # 화면 경계 체크
        
        self.position[0] = new_left
        self.position[2] = new_left + self.current_size
        self.position[1] = self.height - self.current_size - 10
        self.position[3] = self.height - 10
        
    def move(self, command):
        move_speed = self.run_speed if self.is_running else self.walk_speed
        
        # 이동 상태 초기화
        self.is_moving = False
        
        if command['left_pressed']:
            self.is_moving = True
            self.direction = "left"
            self.position[0] = max(0, self.position[0] - move_speed)
            self.position[2] = self.position[0] + self.current_size  # current_size 사용
            self.animation_speed += 1
            
            if self.is_running:
                self.run_state = (self.run_state + 1) % 8
            else:
                self.walk_state = (self.walk_state + 1) % 8
            
        elif command['right_pressed']:
            self.is_moving = True
            self.direction = "right"
            self.position[0] = min(self.width - self.current_size, self.position[0] + move_speed)
            self.position[2] = self.position[0] + self.current_size  # current_size 사용
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