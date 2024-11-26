# Garbagebag.py
import numpy as np
import math

class Garbagebag:
    # 발사 가능한 방향을 클래스 상수로 정의
    THROW_ANGLES = {
        "up": math.pi/2,      # 90도 (수직)
        "up_left": math.pi*2/3,    # 120도 (왼쪽 대각선)
        "up_right": math.pi/3     # 60도 (오른쪽 대각선)
    }

    def __init__(self, character_position, character_size, throw_direction): 
        center_x = (character_position[0] + character_position[2]) / 2

        self.position = np.array([
            center_x - 10,  # 봉투 너비의 절반을 빼서 중앙 정렬
            character_position[1] + character_size/4,  # 캐릭터 크기를 고려한 발사 높이
            center_x + 10,
            character_position[1] + character_size/4 + 20
        ])

        self.speed = 7
        self.state = 'active'

        # 방향에 따른 각도 설정
        angle = self.THROW_ANGLES.get(throw_direction, self.THROW_ANGLES["up"])  # 기본값은 위쪽

        # 삼각함수를 사용하여 수평/수직 속도 계산
        self.vertical_speed = self.speed * math.sin(angle)
        self.horizontal_speed = self.speed * math.cos(angle)
        
        # 왼쪽 대각선인 경우 수평 속도를 음수로
        if throw_direction == "up_left":
            self.horizontal_speed = -abs(self.horizontal_speed)
        
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