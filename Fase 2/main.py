import pygame
import sys
import neat
import os
import pickle
import math

from constantes import *
from entidades import *
from mapa import *

# PYGAME
pygame.init()
pygame.display.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo mais Difícil do Mundo! (Fase 2)")

mapa_surface = pygame.image.load('img/mapa.png').convert_alpha()
mapa_rect = mapa_surface.get_rect(center = (WIDTH//2, HEIGHT//2)) 

# NEAT
GEN = 0

# DRAW WINDOW
def draw_window(win, mapa, bolas, players, moeda, area):
	win.fill(FUNDO)
	win.blit(mapa_surface, mapa_rect)
	pygame.draw.line(win, RED, (area.getx(), area.gety()-11), (area.getx(), area.gety()+11), width = 2)

	for b in bolas:
		b.draw(win)

	moeda.draw(win)

	for p in players:
		if p in players:
			p.targetInfo(win, area, moeda, False)
			p.draw(win)

	# Textos

	# GEN
	score_label = STAT_FONT.render("Gen: " + str(GEN-1), 1, BLACK)
	win.blit(score_label, (30, 10))

	# Vivos
	vivos = VIVOS_FONT.render("Vivos: " + str(len(players)), 1, BLACK)
	win.blit(vivos, (30, 40))

	# W
	contador_ganharam = GANHARAM_FONT.render("W: " + str(ganharam), 1, BLACK)
	win.blit(contador_ganharam, (785, 40))

	# T
	tempo_text = GANHARAM_FONT.render("T: " + str(tempo), 1, BLACK)
	win.blit(tempo_text, (785, 85))

	# ATW
	atw_text = ATW_FONT.render("ATW: " + str(atw), 1, RED)
	win.blit(atw_text, (785, 250))

	# M
	vivosmoeda = []
	for p in players:
		if p.pegouMoeda:
			vivosmoeda.append(p)

	moedapegas_text = MOEDASPEGAS_FONT.render("M: " + str(len(vivosmoeda)), 1, BLACK)
	win.blit(moedapegas_text, (785, 285))

	pygame.display.flip()

def main(genomes, config):

	# NEAT
	global GEN
	global WIN_ON
	global tempo
	global tempo_max
	global ganharam
	global atw

	GEN += 1
	WIN_ON = True
	tempo_max = 8
	ganharam = 0

	# Dá mais X segundos de jogo a cada Y gerações
	if GEN % 15 == 0 and GEN > 0 and GEN < 180:
		tempo_max += 2
	if GEN >= 180:
		tempo_max = 20

	''' Objetos '''

	# Mapa e paredes
	mapa = Mapa()

	# Área que ganha
	area = Win()

	# Moeda
	moeda = Moeda()

	# Bolas Superiores
	bola1 = Bola(67, 1)
	bola3 = Bola(67, 3)
	bola5 = Bola(67, 5)
	bola7 = Bola(67, 7)
	bola9 = Bola(67, 9)
	bola11 = Bola(67, 11)

	# Bolas Inferiores
	bola2 = Bola(306, 2)
	bola4 = Bola(306, 4)
	bola6 = Bola(306, 6)
	bola8 = Bola(306, 8)
	bola10 = Bola(306, 10)
	bola12 = Bola(306, 12)
	bolas = [bola1, bola2, bola3, bola4, bola5, bola6, bola7, bola8, bola9, bola10, bola11, bola12]

	''' Listas '''
	players = []
	nets = []
	ge = []

	# NEAT
	for genomes_id, g in genomes:
		net = neat.nn.FeedForwardNetwork.create(g, config)

		nets.append(net)
		players.append(Player())

		g.fitness = 0
		ge.append(g)

	clock = pygame.time.Clock()
	start_time = pygame.time.get_ticks()
	run = True

	# Main loop
	while run and len(players) > 0:
		if WIN_ON: clock.tick(FPS)

		# Tempo
		tempo = (pygame.time.get_ticks() - start_time) / 1000

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				sys.exit()
				break

		''' Funcionamento básico do jogo '''

		for b in bolas:
			b.move()

		bola1_ind = 0
		bola2_ind = 0

		# NN
		for x, player in enumerate(players):

			for b in bolas:
				player.colisaoBola(b)

			player.colisaoMoeda(moeda)
			player.colisaoParedes(mapa)
			player.colisaoWin(area)

			if tempo >= tempo_max:
				player.timeout = True

			''' Neural Network '''

			# Quais bolas vão ser fornecidas para a NN
			if len(players) > 0:
				for i in range(12):
					if player.getx() <= 210:
						bola1_ind = 0
						bola2_ind = 1
					elif player.getx() >= 716:
						bola1_ind = 11
						bola2_ind = 11
					elif player.getx() >= bolas[i].getx() and player.getx() <= bolas[i+1].getx():
						bola1_ind = i
						bola2_ind = i + 1

			# Inputs da NN
			outputs = nets[players.index(player)].activate( 
				( 
				player.getx(), player.gety(),
				abs(player.target.getx() - player.getx()), abs(player.target.gety() - player.gety()),
				abs(bolas[bola1_ind].getx() - player.getx()), abs(bolas[bola1_ind].gety() - player.gety()),
				abs(bolas[bola2_ind].getx() - player.getx()), abs(bolas[bola2_ind].gety() - player.gety())
				)
			)

			# Movimentos baseado no output (up, down, right)
			if max(outputs) == outputs[0]:
				if outputs[0] > 0.5:
					player.move_up()

			if max(outputs) == outputs[1]:
				if outputs[1] > 0.5:
					player.move_down()

			if max(outputs) == outputs[2]:
				if outputs[2] > 0.5:
					player.move_right()

			''' Fitness '''

			# Timeout
			if player.timeout:
				if player in players:
					removeplayer(nets, ge, x, players, player, 0)

			# Colisão com as bolas	
			if player.colidiu:
				if player in players:
					removeplayer(nets, ge, x, players, player, -5)

			# Passar da moeda sem pegar
			if player.getx() >= moeda.getx() and not player.pegouMoeda:
				if player in players:
					removeplayer(nets, ge, x, players, player, -9)

			# Ganhou
			if player.win:
				if atw >= 3:
					if player in players:
						removeplayer(nets, ge, x, players, player, 99999999)
				else:
					ganharam += 1
					atw += 1

					print("Ganhou!")
					if player in players:
						removeplayer(nets, ge, x, players, player, 1000)

			# Por tempo e posição
			if tempo >= 2.5:
				if player in players:
					if player.getx() <= 186: # Dentro do spawn
						removeplayer(nets, ge, x, players, player, -15)

		# Display
		if WIN_ON:
			draw_window(win, mapa, bolas, players, moeda, area)

# NOVA GERAÇÃO
def removeplayer(nets, ge, x, players, player, valor):

<<<<<<< Updated upstream
	ge[x].fitness = player.fitness + 1000 / player.dist + valor

	# Remove player do jogo
=======
>>>>>>> Stashed changes
	if player in players:
		ge[x].fitness += player.fitness + 1000 / player.dist + valor

		# Remove player do jogo
		nets.pop(players.index(player))
		ge.pop(players.index(player))
		players.pop(players.index(player))

# NEAT
def run(config_file):
	config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_file)

	p = neat.Population(config)

	p.add_reporter(neat.StdOutReporter(True))
	stats = neat.StatisticsReporter()
	p.add_reporter(stats)

	winner = p.run(main, 9999)

	with open('winner.pickle', 'wb') as f:
		pickle.dump(winner, f)

	print('\nBest genome:\n{!s}'.format(winner))

# Config file path
if __name__ == '__main__':
	local_dir = os.path.dirname(__file__)
	config_path = os.path.join(local_dir, 'config-feedforward.txt')
	run(config_path)
