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
        return self.x

    def gety(self):
        return self.y

class Parede:
    def __init__(self, x, y, width, height, index):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.index = index

        #self.surface = pygame.Surface((self.width, self.height))
        
        self.surface = pygame.image.load('img/parede.png').convert_alpha()
        self.surface = pygame.transform.scale(self.surface, (self.width, self.height))
        self.rect = self.surface.get_rect(topleft = (self.x, self.y))

    def draw(self, win):
        win.blit(self.surface, self.rect)

class Mapa:
    def __init__(self):
        #self.parede = Parede(x, y, width, height, index)

        self.parede1 = Parede(162, 129, 8, 345, 'e')
        self.parede2 = Parede(163, 466, 278, 8, 'i')
        self.parede3 = Parede(432, 196 , 8, 278, 'd')
        self.parede4 = Parede(230, 196, 210, 8, 's')
        self.parede5 = Parede(230, 129, 7, 75, 'd')
        self.parede6 = Parede(162, 129, 75, 7, 's')

        # Paredes das bolas
        self.i1 = Parede(180, 214, 243, 1, 's')
        self.i2 = Parede(422, 214, 1, 243, 'd')
        self.i3 = Parede(180, 456, 243, 1, 'i')
        self.i4 = Parede(180, 214, 1, 243, 'e')

        self.paredes = [self.parede1, self.parede2, self.parede3, 
		                self.parede4, self.parede5, self.parede6]

        self.invis = [self.i1, self.i2, self.i3, self.i4]