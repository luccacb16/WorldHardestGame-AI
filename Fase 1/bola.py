import pygame

from constantes import *
from player import *
from mapa import *

class Bola:
    def __init__(self, x, y, type):
        self.x = self.og_x = x
        self.y = self.og_y = y
        self.vel = 4
        self.type = type
        self.count = 0

        self.bola_surface = pygame.image.load('img/bola.png').convert_alpha()
        self.bola_rect = self.bola_surface.get_rect(center = (self.x, self.y))
    
    def draw(self, win):
        self.bola_rect = self.bola_surface.get_rect(center = (self.x, self.y))
        win.blit(self.bola_surface, self.bola_rect)
    
    def move(self):
        self.count += self.vel

        if self.type % 2 == 1:
            self.x += self.vel
            if self.x + self.vel >= 665 or self.x + self.vel <= 235 and self.count != 0:
                self.count = 0
                self.vel *= -1
        else:
            self.x -= self.vel
            if self.x - self.vel >= 665 or self.x - self.vel <= 235 and self.count != 0:
                self.count = 0
                self.vel *= -1

    def reset(self):
        self.x = self.og_x
        self.y = self.og_y
        self.count = 0

    def getx(self):
        return self.x
    
    def gety(self):
        return self.y