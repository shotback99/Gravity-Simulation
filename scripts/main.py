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
add more types of objects and more control over vars of objects -- 6 -- doing
=======
add delatime when program slows and optimise code

validation not working for collections (colours/vectors)
update trail values
make code clean
add comments to help noobs

use diffeent web development IDE
"""
from data.planet import Planet
from data.star import Star
from data.trail import Trail
from data.inputbox import InputBox


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
        self.temporary_objects = []
        self.zoom = 1
        self.delta_time = 0
        self.fps = 60
        self.center = (self.screen_size[0]/2, self.screen_size[1]/2)
        self.zoom_rect = self.screen.get_rect()
        icon = pygame.image.load("data/icon.ico").convert_alpha()# needs to be correct size 32x32
        self.font = pygame.font.Font(None, 50)
        pygame.display.set_icon(icon)
        self.inputs = {"trails": {"spawn rate": 0.1,"radius": 1,"colour": [0, 0, 255], "destroy rate": 0.11},
                       "planets": {"mass": 1, "radius": 5, "colour": [0, 0, 255], "vector": [0, 1]},
                       "suns": {"mass": 1, "radius": 15,"colour": [255, 255, 0], "vector": [0, 0]}
        }
        self.make_input_boxes()

    def run(self):
        self.views = {"menu": True, "game": False, "edit": False}
        while True:
            if self.views["menu"] == True:
                self.menu_view()
            elif self.views["game"] == True:
                self.game_view()
            elif self.views["edit"] == True:
                self.edit_view()

    def make_input_boxes(self):
        offset = self.screen_size[1]*0.01
        spacing = self.screen_size[1]*0.23
        for section, values in self.inputs.items():
            i = 0
            for key, value in values.items(): # not updating values only adding
                i += 1
                if section == "trails":
                    pos = (self.screen_size[0]/4, offset + spacing*i)
                    box = InputBox(pos, value)
                    if key == "colour": box.type["colour"] = True
                    self.inputs[section][key] = box
                elif section == "planets":
                    pos = (self.screen_size[0]/2, offset + spacing*i)
                    box = InputBox(pos, value)
                    if key == "colour": box.type["colour"] = True
                    elif key == "vector": box.type["vector"] = True
                    self.inputs[section][key] = box
                else:
                    pos = (self.screen_size[0]*0.75, offset + spacing*i)
                    box = InputBox(pos, value)
                    if key == "colour": box.type["colour"] = True
                    elif key == "vector": box.type["vector"] = True
                    self.inputs[section][key] = box

    def make_edit_boxes(self):
        boxes = []
        font = pygame.font.Font(None, 75)
        offset = self.screen_size[1]*-0.06
        spacing = self.screen_size[1] * 0.23

        trail = font.render("Trail", False, (255, 255, 255))
        trail_rect = trail.get_rect(center = (self.screen_size[0]/4, self.screen_size[1]*0.1))# could start from 20% but the spacing inbetween could be 10%
        boxes.append([trail, trail_rect])

        planet = font.render("Planet", False, (255, 255, 255))
        planet_rect = planet.get_rect(center = (self.screen_size[0]/2, self.screen_size[1]*0.1))
        boxes.append([planet, planet_rect])

        star = font.render("Star", False, (255, 255, 255))
        star_rect = star.get_rect(center = (self.screen_size[0]*.75, self.screen_size[1]*0.1))
        boxes.append([star, star_rect])

        colour = self.font.render("colour", False, (255, 255, 255))
        colour_rect_1 = colour.get_rect(center = (self.screen_size[0]/4, offset + spacing*3))
        colour_rect_2 = colour.get_rect(center = (self.screen_size[0]/2, offset + spacing*3))
        colour_rect_3 = colour.get_rect(center = (self.screen_size[0]*.75, offset + spacing*3))
        boxes.append([colour, colour_rect_1])
        boxes.append([colour, colour_rect_2])
        boxes.append([colour, colour_rect_3])

        radius = self.font.render("radius", False, (255, 255, 255))
        radius_rect_1 = radius.get_rect(center = (self.screen_size[0]/4, offset + spacing*2))
        radius_rect_2 = radius.get_rect(center = (self.screen_size[0]/2, offset + spacing*2))
        radius_rect_3 = radius.get_rect(center = (self.screen_size[0]*.75, offset + spacing*2))
        boxes.append([radius, radius_rect_1])
        boxes.append([radius, radius_rect_2])
        boxes.append([radius, radius_rect_3])

        mass = self.font.render("mass", False, (255, 255, 255))
        mass_rect_1 = mass.get_rect(center = (self.screen_size[0]/2, offset + spacing))
        mass_rect_2 = mass.get_rect(center = (self.screen_size[0]*.75, offset + spacing))
        boxes.append([mass, mass_rect_1])
        boxes.append([mass, mass_rect_2])

        vector = self.font.render("vector", False, (255, 255, 255))
        vector_rect_1 = vector.get_rect(center = (self.screen_size[0]/2, offset + spacing*4))
        vector_rect_2 = vector.get_rect(center = (self.screen_size[0]*.75, offset + spacing*4))
        boxes.append([vector, vector_rect_1])
        boxes.append([vector, vector_rect_2])

        spawn_rate = self.font.render("spawn rate", False, (255, 255, 255))
        spawn_rect = spawn_rate.get_rect(center = (self.screen_size[0]/4, offset + spacing))
        boxes.append([spawn_rate, spawn_rect])

        destroy_rate = self.font.render("destroy rate", False, (255, 255, 255))
        destroy_rect = spawn_rate.get_rect(center = (self.screen_size[0]/4, offset + spacing*4))
        boxes.append([destroy_rate, destroy_rect])

        return boxes

    def menu_view(self):
        menu_objects = []
        star = Star(10**13, (self.screen_size[0]/2, self.screen_size[1]/2), (0, 0), 15, [255, 255, 0])
        planet = Planet(5*10**9, (500, 500), (0, 1), 5, self.fps, [0, 0, 255], self.inputs["trails"])

        font = pygame.font.Font(None, 100)
        title = font.render("Gravity Simulator", False, (255, 255, 255))
        title_rect = title.get_rect(center = (self.screen_size[0]/2, self.screen_size[1]/6))

        press = self.font.render("press space to start", False, (255, 255, 255))
        press_rect = press.get_rect(center = (self.screen_size[0]/2, self.screen_size[1]*0.85))

        font = pygame.font.Font(None, 30)
        made_by = font.render("made by Lucas Reingo ", False, (255, 255, 255))
        made_by_rect = made_by.get_rect(center = (self.screen_size[0]/2, self.screen_size[1]*0.925))

        menu_objects.append(star)
        menu_objects.append(planet)

        while True:
            self.screen.fill(self.bg_colour)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.views = {"menu": False, "game": True, "edit": False}
                        self.objects = []
                        self.trails = []
                        self.temporary_objects = []
                        return
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()
            for object in menu_objects:
                if isinstance(object, Planet):
                    object.update_trail(self.screen)
                object.draw(self.screen)
                object.update(menu_objects)

            self.screen.blit(title, title_rect)
            self.screen.blit(press, press_rect)
            self.screen.blit(made_by, made_by_rect)

            pygame.display.update()
            self.clock.tick(self.fps)

    def game_view(self):
        scroll_pos = 0
        upd_scroll_pos = False
        place_sun = False
        while True:
            self.screen.fill(self.bg_colour)
            self.m_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.objects = []
                        self.trails = []
                        self.temporary_objects = []
                    if event.key == pygame.K_s: place_sun = True
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()
                    if event.key == pygame.K_SPACE:
                        self.views = {"menu": True, "game": False, "edit": False}
                        return
                    if event.key == pygame.K_e:
                        self.views = {"menu": False, "game": False, "edit": True}
                        return
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_s: place_sun = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if place_sun:
                            mass = 5 * self.inputs["suns"]["mass"].value*10**12 # not updating
                            radius = self.inputs["suns"]["radius"].value
                            colour = self.inputs["suns"]["colour"].value
                            vector = self.inputs["suns"]["vector"].value
                            objects = Star(mass, self.m_pos, vector, radius, colour)
                        else:
                            colour = self.inputs["planets"]["colour"].value
                            radius = self.inputs["planets"]["radius"].value
                            mass = self.inputs["planets"]["mass"].value*10**6
                            vector = self.inputs["planets"]["vector"].value
                            objects = Planet(mass, self.m_pos, vector, radius, self.fps, colour, self.inputs["trails"]) # add values for trails
                        self.objects.append(objects)
                    if event.button == 3:
                        scroll_pos = self.m_pos
                        upd_scroll_pos = True
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 3:
                        upd_scroll_pos = False
            self.upd_screen(upd_scroll_pos, scroll_pos)

    def edit_view(self): # addtext to tell which one is which
        edit_boxes = self.make_edit_boxes()
        while True:
            self.screen.fill((20, 20, 20))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:# male sure this isn't affected by writing
                        self.views = {"menu": False, "game": True, "edit": False}
                        for section in self.inputs.values():
                            for item in section.values():
                                item.selected = False
                                item.bg = (30, 30, 30)
                                item.validate()
                        return
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()
                    for section in self.inputs.values():
                        for item in section.values():
                            if item.selected:
                                if event.key == pygame.K_BACKSPACE:
                                    item.update_input(item.text[:-1], add = False)
                                else:
                                    item.update_input(event.unicode)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for section in self.inputs.values():
                            for item in section.values():
                                item.is_selected(pygame.mouse.get_pos())

            for i, section in enumerate(self.inputs.values()):
                for item in section.values():
                    item.draw(self.screen)
            for box, rect in edit_boxes:
                self.screen.blit(box, rect)
            pygame.display.update()
            self.clock.tick(self.fps)

    def upd_screen(self, upd_scroll_pos, scroll_pos):
        if upd_scroll_pos:
            self.scroll_screen(scroll_pos)
        planets = [planet for planet in self.objects if isinstance(planet, Planet)]
        suns = [sun for sun in self.objects if isinstance(sun, Star)]
        for object in planets:
            if object.collide_with_sun:
                self.temporary_objects.append(object)
                self.objects.remove(object)
            else:
                for trail in object.trails: trail.draw(self.screen)
                object.draw(self.screen)
                object.update_trail(self.screen)
                object.update(self.objects)
        for object in suns:
            object.draw(self.screen)
            object.update(self.objects)
        for object in self.temporary_objects:
            object.local_time = 0
            object.update_trail(self.screen)
        pygame.display.update()
        self.clock.tick(self.fps)

    def scroll_screen(self, scroll_pos):
        scroll_pos = scroll_pos
        mx, my = self.m_pos
        sx, sy = scroll_pos
        dx = mx-sx
        dy = my-sy
        t = pygame.time.get_ticks()
        delta_time = (t - self.delta_time) / 10000000
        self.delta_time = delta_time
        dx /= 100#*= 5 * delta_time
        dy /= 100#*= 5 * delta_time
        self.m_pos = (self.m_pos[0]+dx, self.m_pos[1]+dy)
        for object in self.objects:
            object.position = [object.position[0] + dx, object.position[1] + dy]
            if isinstance(object, Star) or len(object.trails) == 0: continue
            for trail in object.trails:
                trail.position = [trail.position[0] + dx, trail.position[1] + dy]
        if len(self.temporary_objects) > 0:
            for object in self.temporary_objects:
                for trail in object.trails:
                    trail.position = [trail.position[0] + dx, trail.position[1] + dy]

if __name__ == '__main__':
    game = Game()
    game.run()
