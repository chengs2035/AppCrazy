class Player:
    def __init__(self):
        self.score = 0
        self.misses = 0
        self.max_misses = 15
        
    def add_score(self, points=2):
        """增加分数"""
        self.score += points
        
    def add_miss(self):
        """增加未击中次数"""
        self.misses += 1
        
    def is_game_over(self):
        """检查游戏是否结束"""
        return self.misses >= self.max_misses
        
    def get_score(self):
        """获取当前分数"""
        return self.score
        
    def get_misses(self):
        """获取未击中次数"""
        return self.misses 