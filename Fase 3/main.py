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
pygame.display.set_caption("Jogo mais Difícil do Mundo! (Fase 3)")

mapa_surface = pygame.image.load('img/mapa.png').convert_alpha()
mapa_rect = mapa_surface.get_rect(center = (WIDTH//2, HEIGHT//2))

# NEAT
GEN = 0
atw = 0

def draw_window(win, bolas, moeda, players, area):
	# Janela
	win.fill(FUNDO)
	win.blit(mapa_surface, mapa_rect)

	# Objetos

	for b in bolas:
		b.draw(win)
	
	for p in players:
		if p in players:
			p.targetInfo(win, area, moeda, lines=True, dist=True)
			p.draw(win)
			
	moeda.draw(win)

	''' Textos '''

	# ESQUERDA

	# GEN
	gen_text = GEN_FONT.render("Gen: " + str(GEN-1), 1, BLACK)
	win.blit(gen_text, (30, 30))

	# Vivos:
	vivos_text = VIVOS_FONT.render("Vivos: " + str(len(players)), 1, BLACK)
	win.blit(vivos_text, (30, 60))

	# DIREITA
	
	# T
	tempo_text = TEMPO_FONT.render("T: " + str(tempo), 1, BLACK)
	win.blit(tempo_text, (WIDTH-120, 30))
	
	# W
	ganharam_text = TEMPO_FONT.render("W: " + str(ganharam), 1, BLACK)
	win.blit(ganharam_text, (WIDTH-120, 75))

	# ATW
	atw_text = ATW_FONT.render("ATW: " + str(atw), 1, RED)
	win.blit(atw_text, ((WIDTH-120, 120)))
	
	pygame.display.flip()

# -------------------------------------------------------------------------------------------------------

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

	# Objetos
	mapa = Mapa()

	moeda = Moeda()

	area = Win(234, 268, 134, 134)

	bola1 = Bola(198, 301, 1)
	bola2 = Bola(198, 232, 2)
	bola3 = Bola(267, 232, 3)
	bola4 = Bola(336, 232, 4)
	bola5 = Bola(402, 232, 5)
	bola6 = Bola(402, 301, 6)
	bola7 = Bola(402, 370, 7)
	bola8 = Bola(402, 436, 8)
	bola9 = Bola(336, 436, 9)
	bola10 = Bola(267, 436, 10)
	bola11 = Bola(198, 436, 11)

	# Listas
	bolas = [bola1, bola2, bola3, bola4, bola5, bola6, bola7, bola8, bola9, bola10, bola11]

	players = []
	nets = []
	ge = []

	# NEAT
	for genomes_id, genome in genomes:
		net = neat.nn.FeedForwardNetwork.create(genome, config)

		nets.append(net)
		players.append(Player())

		genome.fitness = 0
		ge.append(genome)

	clock = pygame.time.Clock()
	start_time = pygame.time.get_ticks()
	run = True
	
	# Main loop
	while run and len(players) > 0:
		if WIN_ON: clock.tick(FPS)

		# Tempo
		tempo = (pygame.time.get_ticks()-start_time) / 1000

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				sys.exit()
				break

		''' Funcionamento básico do jogo '''

		for b in bolas:
			b.move(mapa)

		# NEAT
		for x, player in enumerate(players):

			# Colisões
			player.colisaoBolas(bolas)
			player.colisaoParedes(mapa)
			player.colisaoMoeda(moeda)
			player.colisaoWin(area)

			''' Neural Network '''

			# Inputs da NN
			outputs = nets[players.index(player)].activate( 
				(
				player.x, player.y,
				(player.target.x - player.x), (player.target.y - player.y),

				bola1.x, bola1.y,
				bola11.x, bola11.y,
				)
			)

			# Movimentos baseado no output (up, down, right, left)
			if max(outputs) == outputs[0]:
				if outputs[0] > 0.5:
					player.move_up()

			if max(outputs) == outputs[1]:
				if outputs[1] > 0.5:
					player.move_down()

			if max(outputs) == outputs[2]:
				if outputs[2] > 0.5:
					player.move_right()
			
			if max(outputs) == outputs[3]:
				if outputs[3] > 0.5:
					player.move_left()

			''' Fitness '''

			# Tempo máximo
			if tempo >= tempo_max:
				removeplayer(nets, ge, x, players, player, 0)
				
			# Colisão com as bolas
			if player.colidiu:
				removeplayer(nets, ge, x, players, player, -5)

			# Ganhou:
			if player.win:
				if atw >= 30:
					removeplayer(nets, ge, x, players, player, 99999999)
				else:
					removeplayer(nets, ge, x, players, player, 5000)
					ganharam += 1
					atw += 1

			# Por tempo e posição
			if tempo >= 6:
				if player.moeda and player.y <= 195: # Pega a moeda e fica parado
					removeplayer(nets, ge, x, players, player, -15)

			if tempo >= tempo_max / 3:	
				if player.rect.colliderect(area.rect) and not player.moeda: # Dentro do area (sem moeda)
					removeplayer(nets, ge, x, players, player, -15)

		if WIN_ON:
			draw_window(win, bolas, moeda, players, area)

# -------------------------------------------------------------------------------------------------------

# NOVA GERAÇÃO
def removeplayer(nets, ge, x, players, player, valor):
	
	if player in players:

		ge[x].fitness += player.fitness +  (2500 / player.dist) + valor

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