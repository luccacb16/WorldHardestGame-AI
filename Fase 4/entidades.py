import pygame
import math

from constantes import *
from mapa import *

# PLAYER
class Player:
    def __init__(self):
        self.x = 501
        self.y = 129
        self.xvel = 4.5
        self.yvel = 4.5

        self.target = self
        self.dist = 999999
        self.fitness = 0

        self.moeda1 = self.moeda2 = self.moeda3 = False
        self.colidiu = False
        self.timeout = False
        self.win = False

        self.surface = pygame.image.load('img/player.png').convert_alpha()
        self.surface = pygame.transform.scale(self.surface, (37, 37))
        self.rect = self.surface.get_rect(center = (self.x, self.y))

    def colisaoParedes(self, mapa):
        for parede in mapa.paredes:
            if self.rect.colliderect(parede.rect):

                if parede.index == 's':
                    self.y += self.yvel

                if parede.index == 'i':
                    self.y -= self.yvel

                if parede.index == 'e':
                    self.x += self.xvel

                if parede.index == 'd':
                    self.x -= self.xvel

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

    def getx(self):
        return self.x

    def gety(self):
        return self.y

    def colisaoBola(self, bola):
        if self.rect.colliderect(bola.rect):
            self.colidiu = True

    def colisaoMoedas(self, moedas):
        if self.rect.colliderect(moedas[0].rect):
            self.moeda1 = True
            self.fitness = 40
        
        if self.rect.colliderect(moedas[1].rect) and self.moeda1:
            self.moeda2 = True
            self.fitness = 80

        if self.rect.colliderect(moedas[2].rect) and self.moeda2:
            self.moeda3 = True
            self.fitness = 120
        
    def colisaoWin(self, area):
        if self.rect.colliderect(area.rect):
            if self.moeda1 and self.moeda2 and self.moeda3:
                self.win = True

    def targetInfo(self, win, area, moedas, switch):
        # Linhas

        if not self.moeda1: # Nenhuma moeda
            self.target = moedas[0]
            color = GREEN

        if self.moeda1: # Moeda1
            self.target = moedas[1]
            color = BLUE

        if self.moeda1 and self.moeda2: # Moeda1 e Moeda2
            self.target = moedas[2]
            color = BLACK

        if self.moeda1 and self.moeda2 and self.moeda3: # Moeda1, Moeda2, Moeda3
            self.target = area
            color = RED
        
        pygame.draw.line(win, color, (self.getx(), self.gety()), (self.target.getx(), self.target.gety()), 2)

        self.dist = math.sqrt ((self.getx() - self.target.getx())**2 + (self.gety() - self.target.gety())**2)

        if switch:

            Xm = ((self.getx() + self.target.getx()) / 2) - 15
            Ym = ((self.gety() + self.target.gety()) / 2) - 15

            dist_text = DIST_FONT.render("d: " +  "{:.2f}".format(self.dist), 1, (0, 0, 0, 191))
            win.blit(dist_text, (Xm, Ym))

# BOLA
class Bola:
    def __init__(self, ini, n):
        self.ini = ini
        self.n = n

        self.r = 49 * n
        self.vel = 1.75

        self.x = self.ogx = 500
        self.y = self.ogy = 502
        
        self.surface = pygame.image.load('img/bola.png').convert_alpha()
        self.rect = self.surface.get_rect(center = (self.x, self.y))

    def draw(self, win):
        self.rect = self.surface.get_rect(center = (self.x, self.y))
        win.blit(self.surface, self.rect)

    def move(self):
        self.ini -= self.vel

        self.x = self.ogx + self.r * math.sin(math.radians(self.ini))
        self.y = self.ogy + self.r * math.cos(math.radians(self.ini))

    def getx(self):
        return self.x

    def gety(self):
        return self.y

# MOEDA
class Moeda:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.surface = pygame.image.load('img/moeda.png').convert_alpha()
        self.rect = self.surface.get_rect(center = (self.x, self.y))

    def draw(self, win):
        win.blit(self.surface, self.rect)

    def getx(self):
        return self.x

    def gety(self):
        return self.y