import pygame
import sys
import neat
import os
import pickle
import math

from constantes import *
from entidades import *
from mapa import *

# MAPA
class Win:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.surface = pygame.Surface((self.width, self.height))
        self.rect = self.surface.get_rect(topleft = (self.x, self.y))

    def getx(self):
        return 230

    def gety(self):
        return 501

class Parede:
    def __init__(self, x, y, width, height, index):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.index = index

        self.surface = pygame.Surface((self.width, self.height))
        self.rect = self.surface.get_rect(topleft = (self.x, self.y))

    def draw(self, win):
        win.blit(self.surface, self.rect)

class Mapa:
    def __init__(self):
        #self.parede = Parede(x, y, width, height, index)

        self.parede1 = Parede(429, 29, 143, 8, 's')
        self.parede2 = Parede(565, 24, 7, 210, 'd')
        self.parede3 = Parede(565, 227, 75, 7, 's')
        self.parede4 = Parede(632, 227, 8, 75, 'd')
        self.parede5 = Parede(632, 294, 75, 8, 's')
        self.parede6 = Parede(700, 294, 7, 75, 'd')
        self.parede7 = Parede(700, 362, 75, 7, 's')
        self.parede8 = Parede(767, 362, 8, 278, 'd')
        self.parede9 = Parede(700, 632, 75, 7, 'i')
        self.parede10 = Parede(700, 632, 8, 75, 'd')
        self.parede11 = Parede(632, 699, 75, 8, 'i')
        self.parede12 = Parede(632, 699, 8, 75, 'd')
        self.parede13 = Parede(362, 767, 278, 7, 'i')
        self.parede14 = Parede(362, 699, 8, 75, 'e')
        self.parede15 = Parede(295, 699, 75, 8, 'i')
        self.parede16 = Parede(295, 632, 7, 75, 'e')
        self.parede17 = Parede(227, 632, 75, 7, 'i')
        self.parede18 = Parede(227, 564, 8, 75, 'e')
        self.parede19 = Parede(227, 362, 8, 75, 'e')
        self.parede20 = Parede(227, 362, 75, 7, 's')
        self.parede21 = Parede(295, 294, 7, 75, 'e') 
        self.parede22 = Parede(295, 294, 75, 8, 's')
        self.parede23 = Parede(362, 227, 8, 75, 'e')
        self.parede24 = Parede(362, 227, 75, 7, 's')
        self.parede25 = Parede(429, 24, 8, 210, 'e')

        self.paredes = [self.parede1, self.parede2, self.parede3, self.parede4, self.parede5, 
                        self.parede6, self.parede7, self.parede8, self.parede9, self.parede10,
                        self.parede11, self.parede12, self.parede13, self.parede14, self.parede15,
                        self.parede16, self.parede17, self.parede18, self.parede19, self.parede20,
                        self.parede21, self.parede22, self.parede23, self.parede24, self.parede25]
