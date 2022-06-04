from math import sqrt, atan2, sin , cos
from scipy.constants import G
from trail import Trail
import pygame
pygame.init()

class Planet:
    def __init__(self, mass, position, velocity, radius, fps, tsr = 0.1, tud = 0.2):
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.colour = (0, 0, 255)
        self.radius = radius
        self.trails = []
        self.fps = fps
        self.trail_spawn_rate = tsr * fps
        self.trail_delete_rate = tud * fps
        self.local_time = 0

    def draw(self, screen):
        pygame.draw.circle(screen, self.colour, self.position, self.radius)
        if len(self.trails) > 0 and sum(self.velocity) != 0:
            check = self.trails[0].upd_timer()
            if check:
                self.trails.pop(0) # returns deleted item
            for trail in self.trails:
                trail.draw(screen)

    def update(self, planets):
        self.local_time += 1
        if self.local_time == self.trail_spawn_rate:
            trail = Trail(self.position, self.trail_delete_rate)
            self.trails.append(trail)
            self.local_time = 0
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
            if (self.radius + planet.radius) < dist*0.8: # separate list if
                self.velocity = (self.velocity[0] - total_x/self.mass, self.velocity[1] - total_y/self.mass)
            else:
                if isinstance(planet, Planet): velocity = (0, 0)
                self.velocity = (self.velocity[0] + total_x/self.mass, self.velocity[1] + total_y/self.mass)
