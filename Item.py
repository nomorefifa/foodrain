# Item.py
import numpy as np
import random

class Item:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.base_fall_speed = 3
        self.position = np.array([0, 0, 0, 0])
        self.item_type = 0 # 0-4: 음식, 5: 쓰레기, 6: 알약
        self.state = 'active'
        self.item_size = 30  # 아이템 크기 조절
        self.reset()
        
    def reset(self):
        # 아이템 크기를 반영한 생성 위치 계산
        x_start = random.randint(0, self.width - self.item_size)
        y_start = random.randint(-200, -20)
        
        self.position = np.array([x_start,y_start,x_start + self.item_size,y_start + self.item_size])

        # 아이템 타입 결정
        # 0-4: 음식, 5: 쓰레기, 6: 알약
        rand_val = random.random()
        if rand_val < 0.3:  # 30%의 확률로 쓰레기 생성
            self.item_type = 5  # 쓰레기
        elif rand_val < 0.33:  # 3%의 확률로 알약 생성 (0.30 ~ 0.33)
            self.item_type = 6  # 알약
        else:  # 67%의 확률로 음식 생성
            self.item_type = random.randint(0, 4)  # 음식 아이템

        self.state = 'active'
        # 각 아이템마다 약간 다른 낙하 속도 설정
        self.fall_speed = self.base_fall_speed + random.uniform(-0.1, 4.0)
        
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