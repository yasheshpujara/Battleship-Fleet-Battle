class Player:
    count = 0
    name = 'Player'

    def __init__(self, name=str(count)):
        self.count += 1
        self.name += name
