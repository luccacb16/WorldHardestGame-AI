import pygame
import math
from constantes import *
from mapa import *

# PLAYER
class Player:
	def __init__(self):
		self.x = 118
		self.y = 185
		self.xvel = 4
		self.yvel = 4

		self.width = 30
		self.height = 30

		self.target = self
		self.dist = 999999
		self.fitness = 0

		self.pegouMoeda = False
		self.colidiu = False
		self.timeout = False
		self.win = False

		self.surface = pygame.image.load('img/player.png').convert_alpha()
		self.surface = pygame.transform.scale(self.surface, (self.width, self.height))
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

				if parede.index == 's':
					self.y += self.yvel

				if parede.index == 'i':
					self.y -= self.yvel

				if parede.index == 'e':
					self.x += self.xvel

				if parede.index == 'd':
					self.x -= self.xvel

	def colisaoBola(self, bola):
		if self.rect.colliderect(bola.rect):
			self.colidiu = True

	def colisaoMoeda(self, moeda):
		if self.rect.colliderect(moeda.rect):
			self.pegouMoeda = True
			self.fitness = 30

	def colisaoWin(self, area):
		if self.rect.colliderect(area.rect):
			if self.pegouMoeda:
				self.win = True

	def targetInfo(self, win, area, moeda, switch):

		# Define o target
		if not self.pegouMoeda:
			self.target = moeda
			color = GREEN
		else:
			self.target = area
			color = BLUE

		# Desenha as linhas
		pygame.draw.line(win, color, (self.getx(), self.gety()), (self.target.getx(), self.target.gety()), 2)

		self.dist = math.sqrt((self.getx() - self.target.getx())**2 + (self.gety() - self.target.gety())**2)

		# Escreve as distâncias
		if switch:
			Xm = ((self.getx() + self.target.getx()) / 2) - 15
			Ym = ((self.gety() + self.target.gety()) / 2) - 15

			dist_text = DIST_FONT.render("d: " + "{:.2f}".format(self.dist), 1, (0, 0, 0, 191))
			win.blit(dist_text, (Xm, Ym))

	def getx(self):
		return self.x

	def gety(self):
		return self.y

# BOLA
class Bola:
	def __init__(self, y, tipo):
		self.x = 212 + (44 * (tipo-1) + 4.5*(tipo-2))
		self.y = y
		self.vel = 3.5
		self.tipo = tipo
		self.count = 0

		self.surface = pygame.image.load('img/bola.png').convert_alpha()
		self.rect = self.surface.get_rect(center = (self.x, self.y))

	def draw(self, win):
		self.rect = self.surface.get_rect(center = (self.x, self.y))
		win.blit(self.surface, self.rect)

	def move(self):
		self.count += self.vel

		if self.tipo % 2 == 1:
			self.y += self.vel
			if self.y + self.vel >= 318 or self.y + self.vel <= 67 and self.count != 0:
				self.count = 0
				self.vel *= -1
		else:
			self.y -= self.vel
			if self.y - self.vel >= 318 or self.y - self.vel <= 67 and self.count != 0:
				self.count = 0
				self.vel *= -1

	def getx(self):
		return self.x

	def gety(self):
		return self.y

# MOEDA
class Moeda:
	def __init__(self):
		self.x = 474
		self.y = 186

		self.width = 24
		self.height = 24

		self.surface = pygame.image.load('img/moeda.png').convert_alpha()
		self.rect = self.surface.get_rect(center = (self.x, self.y))

	def draw(self, win):
		win.blit(self.surface, self.rect)

	def getx(self):
		return self.x

	def gety(self):
		return self.y