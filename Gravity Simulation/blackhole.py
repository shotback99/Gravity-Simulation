class BlackHole:
    def __init__(self, screen_size):
        x, y = screen_size
        self.mass = 10**15
        self.position = (x / 2, y /2)
