import pygame
import sys
import neat
import os

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
atw = 0

# DRAW WINDOW
def draw_window(win, mapa, bolas, players, moeda, area):
	win.fill(FUNDO)
	win.blit(mapa_surface, mapa_rect)

	for b in bolas:
		b.draw(win)

	moeda.draw(win)

	for p in players:
		if p in players:
			p.targetInfo(win, area, moeda, lines=True, dist=True)
			p.draw(win)

	''' Textos '''

	# ESQUERDA

	# GEN
	score_label = STAT_FONT.render("Gen: " + str(GEN-1), 1, BLACK)
	win.blit(score_label, (45, 45))

	# Vivos
	vivos = VIVOS_FONT.render("Vivos: " + str(len(players)), 1, BLACK)
	win.blit(vivos, (45, 75))

	# DIREITA

	# T
	tempo_text = GANHARAM_FONT.render("T: " + str(tempo), 1, BLACK)
	win.blit(tempo_text, (785, 60))
	
	# ATW
	atw_text = ATW_FONT.render("ATW: " + str(atw), 1, RED)
	win.blit(atw_text, (785, 95))

	# W
	contador_ganharam = GANHARAM_FONT.render("W: " + str(ganharam), 1, BLACK)
	win.blit(contador_ganharam, (785, 255))
	
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
	tempo_max = 12
	ganharam = 0

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

		# NN
		for x, player in enumerate(players):

			player.colisaoBolas(bolas)
			player.colisaoMoeda(moeda)
			player.colisaoParedes(mapa)
			player.colisaoWin(area)

			''' Neural Network '''

			# Quais bolas vão ser fornecidas para a NN

			bola1_ind = 0
			bola2_ind = 1

			if len(players) > 0:
				for i in range(12):
					if player.x >= 716:
						bola1_ind = 11
						bola2_ind = 11
					elif player.x >= bolas[i].x and player.x <= bolas[i+1].x:
						bola1_ind = i
						bola2_ind = i + 1

			# Inputs da NN
			outputs = nets[players.index(player)].activate( 
				( 
				player.x, player.y, # Posição do player

				(player.target.x - player.x), (player.target.y - player.y), # Distância do player ao target

				bolas[bola1_ind].x, bolas[bola1_ind].y, # Bola mais perto da esquerda
				bolas[bola2_ind].x, bolas[bola2_ind].y # Distância do player à bola mais perto 2
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

			# Começa nova geração quando o tempo acaba
			if tempo >= tempo_max:
				removeplayer(nets, ge, x, players, player, 0)

			# Colisão com as bolas	
			if player.colidiu:
				removeplayer(nets, ge, x, players, player, -5)

			# Passar da moeda sem pegar
			if player.x >= moeda.x and not player.moeda:
				removeplayer(nets, ge, x, players, player, -10)

			# Ganhou
			if player.win:
				if atw >= 30:
					removeplayer(nets, ge, x, players, player, 99999999)
				else:
					removeplayer(nets, ge, x, players, player, 5000)
					ganharam += 1
					atw += 1

			# Por tempo e posição
			if tempo >= 2.5:
				if player.x <= 186: # Dentro do spawn
					removeplayer(nets, ge, x, players, player, -15)

		# Display
		if WIN_ON:
			draw_window(win, mapa, bolas, players, moeda, area)

# NOVA GERAÇÃO
def removeplayer(nets, ge, x, players, player, valor):

	if player in players:
		ge[x].fitness += player.fitness + (1000 / player.dist) + valor

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

	winner = p.run(main, 150)

	print('\nBest genome:\n{!s}'.format(winner))

# Config file path
if __name__ == '__main__':
	local_dir = os.path.dirname(__file__)
	config_path = os.path.join(local_dir, 'config-feedforward.txt')
	run(config_path)