import pygame
import math
from random import randint

from constantes import *
from mapa import *

# PLAYER
class Player:
    def __init__(self):
        self.x = 501
        self.y = 129
        self.xvel = 4
        self.yvel = 4

        self.target = self
        self.dist = 999999
        self.fitness = 0

        self.moeda = [False, False, False]
        self.colidiu = False
        self.colidiuP = False
        self.win = False

        self.surface = pygame.image.load('img/player.png').convert_alpha()
        self.surface = pygame.transform.scale(self.surface, (37, 37))
        self.rect = self.surface.get_rect(center = (self.x, self.y))

    def draw(self, win):
        self.rect = self.surface.get_rect(center = (self.x, self.y))
        win.blit(self.surface, self.rect)

    def move_up(self):
        self.y -= self.yvel

    def move_down(self):
        self.y += self.yvel

    def move_left(self):
        self.x -= self.xvel

    def move_right(self):
        self.x += self.xvel

    def colisaoParedes(self, mapa):
        for parede in mapa.paredes:
            if self.rect.colliderect(parede.rect):

                self.colidiuP = True

    def colisaoBolas(self, bolas):
        for b in bolas:
            if self.rect.colliderect(b.rect):
                self.colidiu = True

    def colisaoMoedas(self, moedas):
        for i, m in enumerate(moedas):
            if self.rect.colliderect(m.rect):
                self.moeda[i] = True
                self.fitness = 40 * (i+1)
        
    def colisaoWin(self, area):
        if self.rect.colliderect(area.rect):
            if self.moeda == [True, True, True]:
                self.win = True

    def targetInfo(self, win, area, moedas, switch):

        if not self.moeda[0]: # Nenhuma moeda
            self.target = moedas[0]
            color = GREEN

        if self.moeda[0]: # Moeda1
            self.target = moedas[1]
            color = BLUE

        if self.moeda[0] and self.moeda[1]: # Moeda1 e Moeda2
            self.target = moedas[2]
            color = BLACK

        if self.moeda == [True, True, True]: # Moeda1, Moeda2, Moeda3
            self.target = area
            color = RED
        
        pygame.draw.line(win, color, (self.x, self.y), (self.target.x, self.target.y), 2)

        self.dist = math.dist([self.x, self.y], [self.target.x, self.target.y])

        if switch:

            Xm = ((self.x + self.target.x) / 2) - 15
            Ym = ((self.y + self.target.y) / 2) - 15

            dist_text = DIST_FONT.render("d: " +  "{:.2f}".format(self.dist), 1, (0, 0, 0, 191))
            win.blit(dist_text, (Xm, Ym))

# BOLA
class Bola:
    def __init__(self, ini, n):
        self.ini = ini
        self.n = n

        self.r = 49 * n
        self.vel = 1.75

        self.x = 500
        self.y = 502
        
        self.surface = pygame.image.load('img/bola.png').convert_alpha()
        self.rect = self.surface.get_rect(center = (self.x, self.y))

    def draw(self, win):
        self.rect = self.surface.get_rect(center = (self.x, self.y))
        win.blit(self.surface, self.rect)

    def move(self):
        self.ini -= self.vel

        self.x = 500 + self.r * math.sin(math.radians(self.ini))
        self.y = 502 + self.r * math.cos(math.radians(self.ini))

# MOEDA
class Moeda:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.surface = pygame.image.load('img/moeda.png').convert_alpha()
        self.rect = self.surface.get_rect(center = (self.x, self.y))

    def draw(self, win):
        win.blit(self.surface, self.rect)