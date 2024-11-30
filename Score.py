# Score.py
class Score:
    def __init__(self):
        self.score = 0
        self.life = 3  # 기본 생명력
        self.max_life = 3  # 최대 생명력
        self.size_level = 1
        self.size_counter = 0  # 크기 증가를 위한 카운터 추가
        
    def get_size_level(self):
        return self.size_level
    
    def decrease_size_level(self):
        if self.size_level > 1:
            self.size_level -= 1  # 크기 레벨만 감소
            self.size_counter = 0  # 축소 시 카운터 리셋
            return True
        return False
        
    def add_score(self):
        old_level = self.get_size_level()
        self.score += 1
        self.size_counter += 1
        
        if self.size_counter >= 10:  # 10개 음식 수집 시
            if self.increase_size_level():  # 크기 증가 시도
                self.size_counter = 0  # 성공하면 카운터 리셋
            else:
                self.size_counter = 9  # 최대 레벨이면 9개 유지
                
        return old_level != self.get_size_level()  # 레벨 변화 여부 반환
        
    def increase_size_level(self):
        if self.size_level < 5:  # 최대 레벨 제한
            self.size_level += 1
            return True
        return False
    
    def lose_life(self):
        self.life -= 1

    def add_life(self):
        if self.life < self.max_life:
            self.life += 1
            return True
        return False
        
    def game_over(self):
        return self.life <= 0
        
    def get_score(self):
        return self.score
        
    def get_life(self):
        return self.life