import pygame
import re
pygame.init()
"""
finish vector validation
start on rgb validation
start validation for when the input box is empty
fix collisions
USE REGEX
"""
class InputBox:
    def __init__(self, pos, text):
        self.text = str(text)
        self.default = text
        self.value = text
        self.selected = False
        self.bg = (30, 30, 30)
        self.width = 200
        self.height = 100
        self.pos = pos
        self.font = pygame.font.Font(None, 50)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = pos
        self.type = {"colour": False, "vector": False}
        if any(self.type):
            text = self.text.replace("[", "")
            self.text = text.replace("]", "")
        #     if self.type["vector"]:
        #         self.text = convert_vector_string()

    def draw(self, screen):
        pygame.draw.rect(screen, self.bg, self.rect)
        input = self.font.render(f"{self.text}", False, (255, 255, 255))
        input_rect = input.get_rect(center = self.pos)
        screen.blit(input, input_rect)

    def is_selected(self, m_pos):
        if self.rect.collidepoint(m_pos):
            self.selected = True
            self.bg = (40, 40, 40)
            return True
        else:
            self.selected = False
            self.bg = (30, 30, 30)
            return False

    def update_input(self, input, add = True):
        if add:
            self.text += str(input)
        else:
            self.text = input

    def validate(self):
        if self.type["colour"]: # allowed: number between 0 - 255, "," between, 3 values, no alhabet
            if is_colour(self.text):
                self.text = minimal_whitespace(self.text)
                text = self.text.replace(" ", "").split(",")
                self.value = [int(i) for i in text]
            else:
                self.text = str(self.default)
                text = self.text.replace("[", "")
                self.text = text.replace("]", "")
                self.value = self.default
        elif self.type["vector"]: # two values, "," between, no alphabet
            if is_vector(self.text):
                #text = convert_vector_string(self.text)
                text = self.text.replace(" ", "").split(",")
                self.value = [int(i) for i in text]
            else:
                self.text = str(self.default)
                text = self.text.replace("[", "")
                self.text = text.replace("]", "")
                self.value = self.default
        else:
            if is_num(self.text):
                self.value = float(self.text)
            else:
                self.text = str(self.default)
                self.value = self.default

def convert_vector_string(string):
    convert = minimal_whitespace(string)
    convert = convert.split(",")
    if convert[1][1] == "-":
        convert[1] = convert[1].replace("-", "")
    else:
        convert[1] = convert[1].replace("", "-")
    convert = ",".join(convert)
    return convert

def minimal_whitespace(string):
    string = string.replace(" ", "").split(",")
    string = ", ".join(string)
    return string


def is_num(string):
    pattern = r'\d*\.?\d+'
    if re.fullmatch(pattern, string):
        return True
    return False

def is_vector(string):
    pattern = '-?\d+ *, *-?\d+'
    if re.fullmatch(pattern, string):
        return True
    return False

def is_colour(string):
    pattern = "\d{1,3} *, *\d{1,3} *, *\d{1,3}"#'^(?:(?:^|,\s*)([01]?\d\d?|2[0-4]\d|25[0-5])){3}$'
    if re.fullmatch(pattern, string):
        text = string.replace(" ", "").split(",")
        nums = [True if int(i) <= 255 and int(i) >=0 else False for i in text]
        return all(nums)
    return False

if __name__ == '__main__':
    t = "2, 0, 4"# makes num into float
    # print(minimal_whitespace(t))
    # print(convert_vector_string(t))
    print(is_colour(t))

"""
problem needs to be a 3 digit num to work
"""
