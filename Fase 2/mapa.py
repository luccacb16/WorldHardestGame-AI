import pygame
from constantes import *

# MAPA
class Win:
	def __init__(self):
		self.x = 763
		self.y = 142
		self.width = 1
		self.height = 90

		self.surface = pygame.Surface((self.width, self.height))
		self.rect = self.surface.get_rect(topleft = (self.x, self.y))

	def getx(self):
		return self.x

	def gety(self):
		return self.y + 45

class Parede:
	def __init__(self, x, y, width, height, index):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.index = index

		self.surface = pygame.Surface((self.width, self.height))
		self.rect = self.surface.get_rect(topleft = (self.x, self.y))

class Mapa:
	def __init__(self):
		#self.parede = Parede(x, y, width, height, index)

		self.parede1 = Parede(40, 232, 150, 6, 'i')
		self.parede2 = Parede(40, 136, 6, 102, 'e')
		self.parede3 = Parede(40, 136, 150, 6, 's')
		self.parede4 = Parede(184, 40, 6, 102, 'e')
		self.parede5 = Parede(184, 40, 582, 6, 's')

		self.parede6 = Parede(759, 40, 6, 102, 'd')
		self.parede7 = Parede(759, 232, 6, 102, 'd')
		self.parede8 = Parede(184, 328, 582, 6, 'i')
		self.parede9 = Parede(184, 232, 6, 102, 'e')

		self.paredes = [self.parede1, self.parede2, self.parede3, 
		    self.parede4, self.parede5, self.parede6,
		    self.parede7, self.parede8, self.parede9]