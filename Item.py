# Item.py
import numpy as np
import random

class Item:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.fall_speed = 3
        self.position = np.array([0, 0, 0, 0])
        self.item_type = 0
        self.state = 'active'
        self.reset()
        
    # Item.py의 reset 메소드 수정
    def reset(self):
        self.position = np.array([random.randint(0, self.width-20), -20, 0, 0])
        # x1 (이미지 너비가 20이므로)
        # y1 (화면 위에서 시작)
        # x2 (초기화 시 계산)
        # y2 (초기화 시 계산)
        self.position[2] = self.position[0] + 20  # x2 = x1 + width
        self.position[3] = self.position[1] + 20  # y2 = y1 + height
        self.item_type = random.randint(0, 5)  # 0-4: 음식, 5: 쓰레기
        self.state = 'active'
        
    def fall(self):
        self.position[1] += self.fall_speed
        self.position[3] += self.fall_speed
        
        # 화면 밖으로 나가면 리셋
        if self.position[1] > self.height:
            self.reset()
            
    def check_collision(self, character_pos):
        return (self.position[0] < character_pos[2] and 
                self.position[2] > character_pos[0] and 
                self.position[1] < character_pos[3] and 
                self.position[3] > character_pos[1])
    
    def check_bottom(self, height):
        if self.position[3] >= height and self.state == 'active':
            if self.item_type == 5:  # 쓰레기가 바닥에 닿았을 때
                return True
        return False