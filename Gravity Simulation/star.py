from math import sqrt, atan2, sin , cos
from scipy.constants import G
import pygame
pygame.init()

class Star: # bug only one of the stars is being repelled
    def __init__(self, mass, pos, velocity, radius):
        self.mass = mass
        self.position = pos
        self.velocity = velocity
        self.radius = radius
    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 0), self.position, self.radius)

    def update(self, planets):
        self.apply_gravity(planets)
        self.position = (self.position[0] + self.velocity[0], self.position[1] + self.velocity[1])

    def apply_gravity(self, planets):
        total_x = total_y = 0
        for planet in planets:
            if self == planet:continue
            x, y = self.position
            px, py = planet.position

            dist = sqrt((x-px)**2 + (y-py)**2)
            if dist == 0: continue
            force = (G*self.mass * planet.mass) / (dist**2)
            angle = atan2(y-py, x-px)
            total_x = cos(angle) * force
            total_y = sin(angle) * force
            if (self.radius + planet.radius) < dist*0.8:
                self.velocity = (self.velocity[0] - total_x/self.mass, self.velocity[1] - total_y/self.mass)
            else:
                self.velocity = (self.velocity[0] + total_x/self.mass, self.velocity[1] + total_y/self.mass)
