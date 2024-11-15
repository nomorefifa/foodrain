# Garbagabag.py
import numpy as np

class Garbagebag:
    def __init__(self, position):
        self.position = np.array([
            position[0] + 15,  # 캐릭터 중앙에서 발사
            position[1],
            position[0] + 35,
            position[1] + 20
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