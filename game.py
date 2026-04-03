from player import Player
class Game:
    def __init__(self,skin_path):
        self.player=Player(skin_path)
        self.pressed={}
