class Player:
    def __init__(self, name="Player"):
        self.name = name
        self.score = 0
        self.games_played = 0
        self.games_won = 0

    def win_game(self, score):
        self.games_played += 1
        self.games_won += 1
        self.score += score

    def lose_game(self):
        self.games_played += 1