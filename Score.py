# Score.py
class Score:
    def __init__(self):
        self.score = 0
        self.life = 3
        
    def add_score(self):
        self.score += 1
        
    def lose_life(self):
        self.life -= 1
        
    def game_over(self):
        return self.life <= 0
        
    def get_score(self):
        return self.score
        
    def get_life(self):
        return self.life