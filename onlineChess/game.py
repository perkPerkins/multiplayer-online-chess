class Game:
    def __init__(self, id):
        self.player_turn = 0
        self.id = id
        self.ready = False
        self.loser = -1
        self.player_one_name = ""
        self.player_two_name = ""
        self.player_one_move = ""
        self.player_two_move = ""

    def update_loser(self, player):
        self.loser = player

    def update_move(self, player, move):
        if player == 0:
            self.player_one_move = move
            self.player_turn = 1
        else:
            self.player_two_move = move
            self.player_turn = 0

