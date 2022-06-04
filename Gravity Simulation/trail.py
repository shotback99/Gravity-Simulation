import pygame
pygame.init()
class Trail:
    def __init__(self, position, tud):
        self.position = position
        self.time_until_destroy = tud
        self.colour = (0, 0, 255)
        self.radius = 1
    def draw(self, screen):
        pygame.draw.circle(screen, self.colour, self.position, self.radius)
    def upd_timer(self):
        self.time_until_destroy -= 1
        check = self.check_destroy()
        return check
    def check_destroy(self):
        if self.time_until_destroy <= 0:
            return True
        else: return False
