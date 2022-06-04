"""
https://stackoverflow.com/questions/62668614/zooming-in-and-out-with-pygame

graphics -- done
=======
formulae G*M1*m2/R^2 -- done
=======
collisions -- sorta done, glitching for stars -- 4
=======
change list names to objects, and organise a bit so it isn't an eyesore -- 1 -- done
=======
attach trail objects to the object their follwing to make it easier to control when they spawn -- 2 -- done
=======
when increasing still decreases because can be 0.8 -> 0.9 so still decreasing -- 5--done
=======
make the program more efficient, fps drops when zooming -- 3 -- done
=======
add more types of objects and more control over vars of objects -- 6
=======
fix glitch with zooming


use diffeent web development IDE
"""
from planet import Planet
from star import Star
from trail import Trail
from blackhole import BlackHole

from random import uniform
from pyautogui import size
from sys import exit
from math import sqrt, atan2, sin , cos
import pygame
pygame.init()

class Game:
    def __init__(self, WIDTH = 500, HEIGHT = 500, bg_colour = (0, 0, 0)):
        self.screen_size = size()
        self.screen = pygame.display.set_mode((self.screen_size))
        self.clock = pygame.time.Clock()
        self.bg_colour = bg_colour
        self.objects = []
        self.zoom = 1
        self.delta_time = 0
        self.fps = 60
        self.center = (self.screen_size[0]/2, self.screen_size[1]/2)
        self.zoom_rect = self.screen.get_rect()
        icon = pygame.image.load("icon.ico").convert_alpha()# needs to be correct size 32x32
        pygame.display.set_icon(icon)
    def run(self):
        scroll_pos = 0
        upd_scroll_pos = False
        place_sun = False
        zoom = 0.1

        while True:
            self.screen.fill(self.bg_colour)
            self.m_pos = self.convert_mouse_pos(pygame.mouse.get_pos())
            #m_pos = (m_pos[0] * self.zoom, m_pos[1] * self.zoom)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.objects = []
                        self.trails = []
                    if event.key == pygame.K_s: place_sun = True
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_s: place_sun = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if place_sun:
                            objects = Star(10**13, self.m_pos, (0, 0), radius = 15)
                        else:
                            x = uniform(2, 10)
                            objects = Planet(x*10**9, self.m_pos, (0, 1), x, self.fps)
                        self.objects.append(objects)
                    if event.button == 3:
                        scroll_pos = self.m_pos
                        upd_scroll_pos = True
                    if event.button == 4:
                        scroll_pos = self.convert_mouse_pos(self.m_pos)
                        self.zoom -= zoom
                        if self.zoom >= 0:
                            self.upd_zoom_rect()
                        else: self.zoom = 0
                    if event.button == 5:
                        scroll_pos = self.convert_mouse_pos(self.m_pos)
                        self.zoom += zoom
                        if self.zoom <= 1:
                            self.upd_zoom_rect()
                        else: self.zoom = 1
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 3:
                        upd_scroll_pos = False
            self.upd_screen(upd_scroll_pos, scroll_pos)
    def convert_mouse_pos(self, m_pos):
        x, y = self.zoom_rect.topleft
        width, height = self.zoom_rect.size
        screen_width, screen_height = self.screen_size
        mx, my = m_pos
        mx *= width/screen_width# self.zoom wasn't reflecting width and height as it was before shrinking
        my *= height/screen_height
        x += mx
        y += my
        return (x, y)

    def upd_zoom_rect(self):# update zoom_rect to add delta values when scrolling
        screen_x, screen_y = self.screen_size
        width = screen_x * self.zoom
        height = screen_y * self.zoom
        x = self.m_pos[0] - width/2
        y = self.m_pos[1] - height/2
        x = max(x, 0) # makes sure it isn't below 0
        y = max(y, 0)
        if width + x > screen_x:
            width  = screen_x - x
        if height + y > screen_y:
            height  = screen_y - y
        self.zoom_rect = pygame.Rect(x, y, width, height) # makes a smaller rect of the screen

    def upd_screen(self, upd_scroll_pos, scroll_pos):
        if upd_scroll_pos:
            self.scroll_screen(scroll_pos)
        for object in self.objects:
            if isinstance(object, BlackHole):
                continue
            if isinstance(object, Planet):
                for trail in object.trails: trail.draw(self.screen)
            object.draw(self.screen)
            object.update(self.objects)
        if self.zoom != 1:
            subscreen = self.screen.subsurface(self.zoom_rect)
            self.center = (subscreen.get_width()/2, subscreen.get_height()/2)
            self.subscreen = pygame.transform.scale(subscreen, self.screen_size)
            self.screen.blit(self.subscreen, (0, 0))
        pygame.display.update()
        self.clock.tick(self.fps)

    def scroll_screen(self, scroll_pos):
        scroll_pos = self.convert_mouse_pos(scroll_pos)
        mx, my = self.convert_mouse_pos(self.m_pos)
        sx, sy = scroll_pos
        dx = mx-sx
        dy = my-sy
        t = pygame.time.get_ticks()
        delta_time = (t - self.delta_time) / 10000000
        self.delta_time = delta_time
        dx /= 100#*= 5 * delta_time
        dy /= 100#*= 5 * delta_time
        self.m_pos = (self.m_pos[0]+dx, self.m_pos[1]+dy)
        x, y = self.zoom_rect.topleft
        width, height = self.zoom_rect.size
        #self.zoom_rect.topleft = (x+dx, y+dy)
        print(dx, dy)
        for object in self.objects:
            object.position = (object.position[0] + dx, object.position[1] + dy)
            if isinstance(object, Star) or len(object.trails) == 0: continue
            for trail in object.trails:
                trail.position = (trail.position[0] + dx, trail.position[1] + dy)

if __name__ == '__main__':
    game = Game()
    game.run()
