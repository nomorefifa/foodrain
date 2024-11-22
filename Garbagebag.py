# Garbagabag.py
import numpy as np
import math

class Garbagebag:
    def __init__(self, character_position, character_size, throw_direction): 
        # throw_direction: "up", "up_left", "up_right" 중 하나
        center_x = (character_position[0] + character_position[2]) / 2

        self.position = np.array([
            center_x - 10,  # 봉투 너비의 절반을 빼서 중앙 정렬
            character_position[1] + character_size/4,  # 캐릭터 크기를 고려한 발사 높이
            center_x + 10,
            character_position[1] + character_size/4 + 20
        ])

        self.speed = 7

        # 방향에 따른 각도 설정 (라디안)
        if throw_direction == "up":
            angle = math.pi/2  # 90도 (수직)
        elif throw_direction == "up_left":
            angle = math.pi*2/3  # 120도 (왼쪽 대각선)
        elif throw_direction == "up_right":
            angle = math.pi/3  # 60도 (오른쪽 대각선)
        # 삼각함수를 사용하여 수평/수직 속도 계산
        
        self.vertical_speed = self.speed * math.sin(angle)
        self.horizontal_speed = self.speed * math.cos(angle)

        # right 방향일 경우 수평 속도는 양수, left 방향일 경우 음수
        if throw_direction in ["left", "up_left"]:
            self.horizontal_speed = -abs(self.horizontal_speed)    

        self.state = 'active'
        
    def move(self):
        self.position[0] += self.horizontal_speed
        self.position[2] += self.horizontal_speed
        self.position[1] -= self.vertical_speed
        self.position[3] -= self.vertical_speed
        
    def check_collision(self, item_pos):
        return (self.position[0] < item_pos[2] and 
                self.position[2] > item_pos[0] and 
                self.position[1] < item_pos[3] and 
                self.position[3] > item_pos[1])