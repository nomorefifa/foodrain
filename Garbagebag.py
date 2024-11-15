# Garbagabag.py
import numpy as np

class Garbagebag:
    def __init__(self, character_position, character_size): # character_size 매개변수 추가
        # 캐릭터의 중앙에서 봉투가 발사되도록 계산
        center_x = (character_position[0] + character_position[2]) / 2
        self.position = np.array([
            center_x - 10,  # 봉투 너비의 절반을 빼서 중앙 정렬
            character_position[1] + character_size/4,  # 캐릭터 크기를 고려한 발사 높이
            center_x + 10,
            character_position[1] + character_size/4 + 20
        ])
        self.speed = 7
        self.state = 'active'
        
    def move(self):
        # 위로 이동
        self.position[1] -= self.speed
        self.position[3] -= self.speed
        
    def check_collision(self, item_pos):
        return (self.position[0] < item_pos[2] and 
                self.position[2] > item_pos[0] and 
                self.position[1] < item_pos[3] and 
                self.position[3] > item_pos[1])