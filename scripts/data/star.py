from math import sqrt, atan2, sin , cos
from scipy.constants import G
from data.planet import Planet
import numpy as np
import pygame
pygame.init()

class Star: # bug only one of the stars is being repelled
    def __init__(self, mass, pos, velocity, radius, colour):
        self.mass = mass
        self.position = list(pos)
        self.velocity = list(velocity)
        self.colour = colour
        self.radius = radius
    def draw(self, screen):
        pygame.draw.circle(screen, self.colour, self.position, self.radius)

    def update(self, planets):
        self.apply_gravity(planets)
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

    def apply_gravity(self, planets):
        total_x = total_y = 0
        ax = ay = 0
        for planet in planets:
            if self == planet:continue
            x, y = self.position
            px, py = planet.position

            dist = sqrt((x-px)**2 + (y-py)**2)
            if dist == 0 or self.mass <= 0 or planet.mass <= 0: continue

            force = (G*self.mass * planet.mass) / (dist**2)
            angle = atan2(y-py, x-px)
            total_x = cos(angle) * force
            total_y = sin(angle) * force

            if (self.radius + planet.radius) >= dist: # colliding
                self.collision(dist, planet)
            else:
                # applies gravitational force
                self.velocity[0] -= total_x/self.mass
                self.velocity[1] -= total_y/self.mass # f = ma

    def collision(self, dist, planet):
        if isinstance(planet, Planet):
            planet.collide_with_sun = True
        overlap = dist - (self.radius + planet.radius)
        delta_pos = sqrt(overlap**2/2)
        dx = delta_pos/10
        dy = delta_pos/10
        if self.position[0] > 0:
            dx *= -1
        if self.position[1] > 0:
            dy *= -1

        planet.position[0] += dx
        planet.position[1] += dy

        total_mass = self.mass + planet.mass
        v1 = np.asarray(self.velocity)
        v2 = np.asarray(planet.velocity)
        vector = -1*planet.mass/total_mass*np.inner(v1 - v2, v1 - v2)/np.sum((v1 - v2)**2)*(v1 - v2)
        x, y = list(vector)
        self.velocity[0] += x
        self.velocity[1] += y
