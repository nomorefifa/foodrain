# Score.py
class Score:
    def __init__(self):
        self.score = 0
        self.life = 3
        self.max_life = 3  # 최대 생명력 설정
        self.size_level = 1  # 크기 레벨 추가
        self.max_level = 5  # 최대 레벨 설정
        
    def add_score(self):
        self.score += 1
        # 최대 레벨 제한을 둠
        new_level = min((self.score // 10) + 1, self.max_level)
        # 10점마다 size_level 증가
        level_changed = new_level != self.size_level
        self.size_level = new_level
        return level_changed  # 레벨이 변경되었을 때만 True 반환
    
    def get_size_level(self):
        return self.size_level
        
    def lose_life(self):
        self.life -= 1

    def add_life(self):
        if self.life < self.max_life:  # 최대 생명력을 초과하지 않도록
            self.life += 1
            return True
        return False
        
    def game_over(self):
        return self.life <= 0
        
    def get_score(self):
        return self.score
        
    def get_life(self):
        return self.life