# Score.py
class Score:
    def __init__(self):
        self.score = 0
        self.life = 3  # 기본 생명력
        self.max_life = 3  # 최대 생명력
        
    def get_size_level(self):
        # 크기 레벨은 점수에 따라 계산 (1~5)
        return min((self.score // 10) + 1, 5)
        
    def add_score(self):
        old_level = self.get_size_level()
        self.score += 1
        return old_level != self.get_size_level()  # 레벨 변화 여부 반환
        
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