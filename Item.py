# Item.py
import numpy as np
import random

class Item:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.base_fall_speed = 3
        self.position = np.array([0, 0, 0, 0])
        self.item_type = 0
        self.state = 'active'
        self.reset()
        
    # Item.py의 reset 메소드 수정
    def reset(self):
        # x 위치는 화면 내에서 랜덤하게 설정
        x_start = random.randint(0, self.width - 20)
        # y 위치를 랜덤하게 설정 (-150 ~ -20 사이)
        y_start = random.randint(-200, -20)
        
        self.position = np.array([
            x_start,      # x1
            y_start,      # y1
            x_start + 20, # x2 (너비 20)
            y_start + 20  # y2 (높이 20)
        ])

        # 0-4: 음식, 5: 쓰레기
        # 쓰레기가 나올 확률을 높임 (약 30% 확률)
        if random.random() < 0.3:  # 30%의 확률로 쓰레기 생성
            self.item_type = 5  # 쓰레기
        else:  # 70%의 확률로 음식 생성
            self.item_type = random.randint(0, 4)  # 음식 아이템
        self.state = 'active'
        # 각 아이템마다 약간 다른 낙하 속도 설정
        self.fall_speed = self.base_fall_speed + random.uniform(0.1, 2.0)
        
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