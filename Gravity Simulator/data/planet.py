from math import sqrt, atan2, sin , cos, tan, radians
from scipy.constants import G
import numpy as np
from data.trail import Trail
import pygame
pygame.init()

class Planet:
    def __init__(self, mass, position, velocity, radius, fps, colour, trail_values):
        self.mass = mass
        self.position = list(position)
        self.velocity = list(velocity)
        self.colour = colour
        self.radius = radius
        self.trails = []
        self.fps = fps
        self.trail_spawn_rate = trail_values["spawn rate"].value * fps
        self.trail_delete_rate = trail_values["destroy rate"].value * fps
        self.trail_radius = trail_values["radius"].value
        self.trail_colour = trail_values["colour"].value
        self.local_time = 0
        self.collide_with_sun = False

    def draw(self, screen):
        pygame.draw.circle(screen, self.colour, self.position, self.radius)

    def update_trail(self, screen):
        if len(self.trails) > 0 and sum(self.velocity) != 0:
            check = self.trails[0].upd_timer()
            if check:
                self.trails.pop(0) # returns deleted item
            for trail in self.trails:
                trail.draw(screen)
        self.local_time += 1
        if self.local_time == self.trail_spawn_rate:
            trail = Trail(self.position, self.trail_delete_rate, self.trail_colour, self.trail_radius)
            self.trails.append(trail)
            self.local_time = 0
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
