import math
import _thread as thread
from playsound import playsound 

class Agente:

	def __init__ (self, caverna):

		self.resetaAgente(caverna)

	def resetaAgente (self, caverna):

		self.tiro = True # Munição do agente
		self.matar = False # Indica se o agente quer matar o Wumpus

		self.desempenho = 0

		self.salasConhecidas = [[[] for i in range(4)] for j in range(4)] # Salas que vão sendo conhecidas gradualmente
		self.salasConhecidas[3][0].append('agente')
		
		self.caverna = caverna # Uma cópia da caverna original

		self.posicao = (3, 0) # A posição do agente, inicialmente (3, 0)
		self.posicaoWumpus = -1 # A posição do Wumpus, inicialmente desconhecida

		self.direcao = 'direita' # Posição do agente, inicialmente direita

		self.status = 'Aguardando' # Status a ser exibido na interface, inicialmente, 'Aguardando...'

		self.achouWumpus = False # Indica se ele já encontrou a localização do Wumpus

		self.caminho = [] # Caminho que ele deve percorrer a cada iteração. Será alterado durante a execução
		self.indiceCaminho = 0 # Indice no caminho no qual o agente se encontra

	# Recebe um vetor de caminhos, calcula seus custos e os ordena crescentemente
	def ordenaCustos (self, destinos):

		custos = []
		i = 0

		for sala in destinos:

			custos.append(0)

			if sala[2] == 'cima': #Cima

				if self.direcao == 'baixo':
					custos[i] += 2

				elif self.direcao == 'direita' or self.direcao == 'esquerda':
					custos[i] += 1

			elif sala[2] == 'baixo': #Baixo

				if self.direcao == 'cima':
					custos[i] += 2

				elif self.direcao == 'direita' or self.direcao == 'esquerda':
					custos[i] += 1

			elif sala[2] == 'esquerda': #Esquerda

				if self.direcao == 'direita':
					custos[i] += 2

				elif self.direcao == 'cima' or self.direcao == 'baixo':
					custos[i] += 1

			elif sala[2] == 'direita': #Direita

				if self.direcao == 'esquerda':
					custos[i] += 2

				elif self.direcao == 'cima' or self.direcao == 'baixo':
					custos[i] += 1

			i += 1

		return [x for _,x in sorted(zip(custos, destinos))], sorted(custos)

	# Recebe uma posição de destino e um dicionário de movimentações e calcula o custo do caminho até a posição atual do agente
	def calculaCusto (self, caminhos, destino):

		custo = 0

		atual = destino

		while atual != (self.posicao[0], self.posicao[1], self.direcao):

			custo += 1

			direcao = caminhos[atual][2]

			if atual[2] == 'cima': #Cima

				if direcao == 'baixo':
					custo += 2

				elif direcao == 'direita' or direcao == 'esquerda':
					custo += 1

			elif atual[2] == 'baixo': #Baixo

				if direcao == 'cima':
					custo += 2

				elif direcao == 'direita' or direcao == 'esquerda':
					custo += 1

			elif atual[2] == 'esquerda': #Esquerda

				if direcao == 'direita':
					custo += 2

				elif direcao == 'cima' or direcao == 'baixo':
					custo += 1

			elif atual[2] == 'direita': #Direita

				if direcao == 'esquerda':
					custo += 2

				elif direcao == 'cima' or direcao == 'baixo':
					custo += 1

			atual = caminhos[atual]

		return custo

	# Recebe uma posição de destino e um dicionário de movimentações e constrói o caminho até a posição atual do agente
	def calculaCaminho (self, caminhos, destino):

		atual = destino
		caminho = []

		while atual != (self.posicao[0], self.posicao[1], self.direcao):

			caminho.append((atual[0], atual[1], atual[2]))
			atual = caminhos[atual]

		caminho.reverse()

		return caminho

	# Aplica uma busca em largura a partir da posição atual do agente para descobrir todos os caminhos que levam a salas ainda não visitadas
	def buscaLargura (self):

		i = self.posicao[0]
		j = self.posicao[1]

		borda = []
		destinos= []
		visitados = []
		vertices = {} # sala : pai

		borda.append((i, j, self.direcao))

		# Enquanto a borda não está vazia, enfileira vértices não visitados, lista possíveis destinos para o agente e contrói um dicionário que mostra as movimentações realizadas entre cada sala
		while len(borda) > 0:

			sala = borda.pop(0)

			if sala not in visitados:

				visitados.append(sala)

				if sala[0] > 0:
					if (sala[0]-1, sala[1], 'cima') not in vertices.keys():
						vertices[(sala[0]-1, sala[1], 'cima')] = (sala[0], sala[1], sala[2])
				
					if 'visitada' in self.salasConhecidas[sala[0]-1][sala[1]]:
						borda.append((sala[0]-1, sala[1], 'cima'))

					elif '~w' in self.salasConhecidas[sala[0]-1][sala[1]] and '~p' in self.salasConhecidas[sala[0]-1][sala[1]]:
						destinos.append((sala[0]-1, sala[1], 'cima'))

				if sala[0] < 3:
					if (sala[0]+1, sala[1], 'baixo') not in vertices.keys():
						vertices[(sala[0]+1, sala[1], 'baixo')] = (sala[0], sala[1], sala[2])

					if 'visitada' in self.salasConhecidas[sala[0]+1][sala[1]]:
						borda.append((sala[0]+1, sala[1], 'baixo'))

					elif '~w' in self.salasConhecidas[sala[0]+1][sala[1]] and '~p' in self.salasConhecidas[sala[0]+1][sala[1]]:
						destinos.append((sala[0]+1, sala[1], 'baixo'))
				
				if sala[1] > 0:
					if (sala[0], sala[1]-1, 'esquerda') not in vertices.keys():
						vertices[(sala[0], sala[1]-1, 'esquerda')] = (sala[0], sala[1], sala[2])

					if 'visitada' in self.salasConhecidas[sala[0]][sala[1]-1]:
						borda.append((sala[0], sala[1]-1, 'esquerda'))

					elif '~w' in self.salasConhecidas[sala[0]][sala[1]-1] and '~p' in self.salasConhecidas[sala[0]][sala[1]-1]:
						destinos.append((sala[0], sala[1]-1, 'esquerda'))
				
				if sala[1] < 3:
					if (sala[0], sala[1]+1, 'direita') not in vertices.keys():
						vertices[(sala[0], sala[1]+1, 'direita')] = (sala[0], sala[1], sala[2])

					if 'visitada' in self.salasConhecidas[sala[0]][sala[1]+1]:
						borda.append((sala[0], sala[1]+1, 'direita'))

					elif '~w' in self.salasConhecidas[sala[0]][sala[1]+1] and '~p' in self.salasConhecidas[sala[0]][sala[1]+1]:
						destinos.append((sala[0], sala[1]+1, 'direita'))

		return vertices, destinos

	# Realiza uma busca em largura para encontrar o primeiro caminho até o Wumpus, que não passe por nenhum poço
	def calculaCaminhoWumpus (self):

		caminho = []

		# Se a posição do Wumpus não é conhecida
		if self.posicaoWumpus == -1:

			i = 0

			while i < 4:
				for j in range(4):

					# Escolhe a primeira posição onde o Wumpus pode estar
					if 'wumpus?' in self.salasConhecidas[i][j]:
						self.posicaoWumpus = (i, j)
						i = 5
						break

				i += 1

		i = self.posicao[0]
		j = self.posicao[1]

		borda = []
		visitados = []
		vertices = {} # sala : pai

		borda.append((i, j, self.direcao))

		while len(borda) > 0:

			sala = borda.pop(0)

			if sala not in visitados:

				visitados.append(sala)

				if sala[0] > 0:
					if (sala[0]-1, sala[1], 'cima') not in vertices.keys():
						vertices[(sala[0]-1, sala[1], 'cima')] = (sala[0], sala[1], sala[2])
				
					if (sala[0]-1, sala[1]) == self.posicaoWumpus:
						destino = sala
						break

					elif '~w' in self.salasConhecidas[sala[0]-1][sala[1]] and '~p' in self.salasConhecidas[sala[0]-1][sala[1]] and 'visitada' in self.salasConhecidas[sala[0]-1][sala[1]]:
						borda.append((sala[0]-1, sala[1], 'cima'))

				if sala[0] < 3:
					if (sala[0]+1, sala[1], 'baixo') not in vertices.keys():
						vertices[(sala[0]+1, sala[1], 'baixo')] = (sala[0], sala[1], sala[2])
				
					if (sala[0]+1, sala[1]) == self.posicaoWumpus:
						destino = sala
						break

					elif '~w' in self.salasConhecidas[sala[0]+1][sala[1]] and '~p' in self.salasConhecidas[sala[0]+1][sala[1]] and 'visitada' in self.salasConhecidas[sala[0]+1][sala[1]]:
						borda.append((sala[0]+1, sala[1], 'baixo'))
				
				if sala[1] > 0:
					if (sala[0], sala[1]-1, 'esquerda') not in vertices.keys():
						vertices[(sala[0], sala[1]-1, 'esquerda')] = (sala[0], sala[1], sala[2])
				
					if (sala[0], sala[1]-1) == self.posicaoWumpus:
						destino = sala
						break

					elif '~w' in self.salasConhecidas[sala[0]][sala[1]-1] and '~p' in self.salasConhecidas[sala[0]][sala[1]-1] and 'visitada' in self.salasConhecidas[sala[0]][sala[1]-1]:
						borda.append((sala[0], sala[1]-1, 'esquerda'))
				
				if sala[1] < 3:
					if (sala[0], sala[1]+1, 'direita') not in vertices.keys():
						vertices[(sala[0], sala[1]+1, 'direita')] = (sala[0], sala[1], sala[2])
				
					if (sala[0], sala[1]+1) == self.posicaoWumpus:
						destino = sala
						break

					elif '~w' in self.salasConhecidas[sala[0]][sala[1]+1] and '~p' in self.salasConhecidas[sala[0]][sala[1]+1] and 'visitada' in self.salasConhecidas[sala[0]][sala[1]+1]:
						borda.append((sala[0], sala[1]+1, 'direita'))

		# Com o destino definido, constrói o caminho do agente até a sala desejada
		caminho = self.calculaCaminho(vertices, destino)

		return caminho

	# Realiza uma busca em largura para encontrar o primeiro caminho até alguma sala não visitada, ignorando que nela possa haver um poço ou Wumpus
	def calculaCaminhoChute (self):

		caminho = []

		i = self.posicao[0]
		j = self.posicao[1]

		borda = []
		visitados = []
		vertices = {} # sala : pai

		borda.append((i, j, self.direcao))

		while len(borda) > 0:

			sala = borda.pop(0)

			if sala not in visitados:

				visitados.append(sala)

				if sala[0] > 0:
					if (sala[0]-1, sala[1], 'cima') not in vertices.keys():
						vertices[(sala[0]-1, sala[1], 'cima')] = (sala[0], sala[1], sala[2])
				
					if 'visitada' not in self.salasConhecidas[sala[0]-1][sala[1]]:
						destino = (sala[0]-1, sala[1], 'cima')
						break

					elif '~w' in self.salasConhecidas[sala[0]-1][sala[1]] and '~p' in self.salasConhecidas[sala[0]-1][sala[1]] and 'visitada' in self.salasConhecidas[sala[0]-1][sala[1]]:
						borda.append((sala[0]-1, sala[1], 'cima'))

				if sala[0] < 3:
					if (sala[0]+1, sala[1], 'baixo') not in vertices.keys():
						vertices[(sala[0]+1, sala[1], 'baixo')] = (sala[0], sala[1], sala[2])
				
					if 'visitada' not in self.salasConhecidas[sala[0]+1][sala[1]]:
						destino = (sala[0]+1, sala[1], 'baixo')
						break

					elif '~w' in self.salasConhecidas[sala[0]+1][sala[1]] and '~p' in self.salasConhecidas[sala[0]+1][sala[1]] and 'visitada' in self.salasConhecidas[sala[0]+1][sala[1]]:
						borda.append((sala[0]+1, sala[1], 'baixo'))
				
				if sala[1] > 0:
					if (sala[0], sala[1]-1, 'esquerda') not in vertices.keys():
						vertices[(sala[0], sala[1]-1, 'esquerda')] = (sala[0], sala[1], sala[2])
				
					if 'visitada' not in self.salasConhecidas[sala[0]][sala[1]-1]:
						destino = (sala[0], sala[1]-1, 'esquerda')
						break

					elif '~w' in self.salasConhecidas[sala[0]][sala[1]-1] and '~p' in self.salasConhecidas[sala[0]][sala[1]-1] and 'visitada' in self.salasConhecidas[sala[0]][sala[1]-1]:
						borda.append((sala[0], sala[1]-1, 'esquerda'))
				
				if sala[1] < 3:
					if (sala[0], sala[1]+1, 'direita') not in vertices.keys():
						vertices[(sala[0], sala[1]+1, 'direita')] = (sala[0], sala[1], sala[2])
				
					if 'visitada' not in self.salasConhecidas[sala[0]][sala[1]+1]:
						destino = (sala[0], sala[1]+1, 'direita')
						break

					elif '~w' in self.salasConhecidas[sala[0]][sala[1]+1] and '~p' in self.salasConhecidas[sala[0]][sala[1]+1] and 'visitada' in self.salasConhecidas[sala[0]][sala[1]+1]:
						borda.append((sala[0], sala[1]+1, 'direita'))

		# Com o destino definido, constrói o caminho do agente até a sala desejada
		caminho = self.calculaCaminho(vertices, destino)

		return caminho

	# Calcula o menor caminho até uma sala não conhecida e segura (sem suspeita de poço ou Wumpus)
	def proximoPasso(self):

		self.status = 'Pensando...'
		
		i = self.posicao[0]
		j = self.posicao[1]

		# Os possíveis destinos são calculados utilizando uma busca em largura
		caminhos, destinos = self.buscaLargura()

		custos = []

		for sala in destinos:

			# Calcula o custo de cada caminho
			custos.append(self.calculaCusto(caminhos, sala))

		if len(destinos) > 0:
			
			# Retorna o menor caminho
			destino = [x for _,x in sorted(zip(custos, destinos))][0]
			return self.calculaCaminho(caminhos, destino)

		# Caso não haja nenhum possível destino, retorna -1, indicando que o agente precisará chutar
		return -1

	# Recebe a posição adjacente para a qual o agente deve se locomover, realiza a movimentação e modifica o desempenho do agente
	def andar (self, destino):

		direcao = destino[2]

		custo = 0

		if self.direcao == 'cima': #Cima

			if direcao == 'baixo':
				custo += 2

			elif direcao == 'direita' or direcao == 'esquerda':
				custo += 1

		elif self.direcao == 'baixo': #Baixo

			if direcao == 'cima':
				custo += 2

			elif direcao == 'direita' or direcao == 'esquerda':
				custo += 1

		elif self.direcao == 'esquerda': #Esquerda

			if direcao == 'direita':
				custo += 2

			elif direcao == 'cima' or direcao == 'baixo':
				custo += 1

		elif self.direcao == 'direita': #Direita

			if direcao == 'esquerda':
				custo += 2

			elif direcao == 'cima' or direcao == 'baixo':
				custo += 1

		custo += 1

		self.salasConhecidas[self.posicao[0]][self.posicao[1]].remove('agente') 

		self.status = ''
		if self.direcao != direcao: self.status += 'Virou para '+direcao+'\n'
		self.status += 'Andou!'

		self.posicao = (destino[0], destino[1], destino[2])
		self.direcao = destino[2]
		self.desempenho -= custo
		self.indiceCaminho += 1

		self.salasConhecidas[self.posicao[0]][self.posicao[1]].append('agente')
		
	# Agarra o ouro, altera o desempenho e toca a fanfarra da vitória
	def agarrar(self):

		self.desempenho += 1000

		self.status = 'Agarrou!'
		thread.start_new_thread(soundFX, ('Audio/zelda_fanfarre.mp3', False))

	# Atira no Wumpus
	def atirar(self):
		
		self.status = 'Atirou!'
		self.desempenho -= 10
		self.tiro = False

		# Se o agente estiver na mesma linha ou coluna que o Wumpus, acertará o tiro
		if self.posicaoWumpus != -1:

			if self.posicao[1] == self.posicaoWumpus[1]:
				remove(self.caverna[self.posicaoWumpus[0]][self.posicaoWumpus[1]], 'wumpus')
				self.caverna[self.posicaoWumpus[0]][self.posicaoWumpus[1]].append('wumpusmorto')
				remove(self.salasConhecidas[self.posicaoWumpus[0]][self.posicaoWumpus[1]], 'wumpus')
				self.salasConhecidas[self.posicaoWumpus[0]][self.posicaoWumpus[1]].append('wumpusmorto')
				self.salasConhecidas[self.posicaoWumpus[0]][self.posicaoWumpus[1]].append('~w')
				thread.start_new_thread(soundFX, ('Audio/wilhelm_scream.mp3', False))

			if self.posicao[0] == self.posicaoWumpus[0]:
				remove(self.caverna[self.posicaoWumpus[0]][self.posicaoWumpus[1]], 'wumpus')
				self.caverna[self.posicaoWumpus[0]][self.posicaoWumpus[1]].append('wumpusmorto')
				remove(self.salasConhecidas[self.posicaoWumpus[0]][self.posicaoWumpus[1]], 'wumpus')
				self.salasConhecidas[self.posicaoWumpus[0]][self.posicaoWumpus[1]].append('wumpusmorto')
				self.salasConhecidas[self.posicaoWumpus[0]][self.posicaoWumpus[1]].append('~w')
				thread.start_new_thread(soundFX, ('Audio/wilhelm_scream.mp3', False))

		else:
			print ('Não sei cadê o bixo :(')

	# Recebe um status interrogativo e verifica se sua versão negativa está na posição (i, j) da caverna
	def verificaIncerteza (self, status, i, j):

		if status == 'wumpus?':
			if '~w' not in self.salasConhecidas[i][j]:
				return True
			else:
				return False

		elif status == 'poço?':
			if '~p' not in self.salasConhecidas[i][j]:
				return True
			else:
				return False

		return True

	# Remove um determinado estatus de todas as salas conhecidas, além de assegurar asserções sobre a posição o Wumpus
	def removeIncerteza(self, status):

		for i in range(4):
			for j in range(4):
				if status in self.salasConhecidas[i][j]:
					self.salasConhecidas[i][j].remove(status)

				if 'wumpus' not in self.salasConhecidas[i][j]:
					
					if status == 'wumpus?':
						self.achouWumpus = True
						adiciona(self.salasConhecidas[i][j], '~w')

				else:
					self.posicaoWumpus = (i, j)

	# Realiza inferencias sobre os arredores de uma determinada sala
	def inferirSalas(self, status):
		
		i = self.posicao[0]
		j = self.posicao[1]

		if i == 0: # cima
				
			if self.verificaIncerteza(status, i+1, j):
				adiciona(self.salasConhecidas[i+1][j], status)

		elif i == 1 or i == 2: #meio
			
			if self.verificaIncerteza(status, i+1, j):
				adiciona(self.salasConhecidas[i+1][j], status)
			if self.verificaIncerteza(status, i-1, j):
				adiciona(self.salasConhecidas[i-1][j], status)

		else: # i == 3 baixo

			if self.verificaIncerteza(status, i-1, j):
				adiciona(self.salasConhecidas[i-1][j], status)

		if j == 0:
			if self.verificaIncerteza(status, i, j+1):
				adiciona(self.salasConhecidas[i][j+1], status)

		elif j == 1 or j == 2:
			if self.verificaIncerteza(status, i, j+1):
				adiciona(self.salasConhecidas[i][j+1], status)
			if self.verificaIncerteza(status, i, j-1):
				adiciona(self.salasConhecidas[i][j-1], status)

		else: #j == 3
			if self.verificaIncerteza(status, i, j-1):
				adiciona(self.salasConhecidas[i][j-1], status)

	# Tenta descobrir a poição do Wumpus ou de um poço, a partir de uma posição com fedor ou brisa, dadas suas diagonais conhecidas
	def infereDiagonais (self, status):

		i = self.posicao[0]
		j = self.posicao[1]

		diagonais = [0, 0, 0, 0]

		#cima esquerda
		if i > 0 and j > 0:
			diagonais[0] = (i-1, j-1, self.salasConhecidas[i-1][j-1])

		#cima direita
		if i > 0 and j < 3:
			diagonais[1] = (i-1, j+1, self.salasConhecidas[i-1][j+1])

		#baixo esquerda
		if i < 3 and j > 0:
			diagonais[2] = (i+1, j-1, self.salasConhecidas[i+1][j-1])

		#baixo direita
		if i < 3 and j < 3:
			diagonais[3] = (i+1, j+1, self.salasConhecidas[i+1][j+1])

		if not self.achouWumpus and status == 'fedor':

			if diagonais[0] != 0 and 'fedor' in diagonais[0][2]:
				if 'visitada' in self.salasConhecidas[i][j-1]:
					adiciona(self.salasConhecidas[i-1][j], 'wumpus')
					adiciona(self.salasConhecidas[i][j-1], '~w')
					self.removeIncerteza('wumpus?')

				elif 'visitada' in self.salasConhecidas[i-1][j]:
					adiciona(self.salasConhecidas[i][j-1], 'wumpus')
					adiciona(self.salasConhecidas[i-1][j], '~w')
					self.removeIncerteza('wumpus?')

			if diagonais[1] != 0 and 'fedor' in diagonais[1][2]:
				if 'visitada' in self.salasConhecidas[i][j+1]:
					adiciona(self.salasConhecidas[i-1][j], 'wumpus')
					adiciona(self.salasConhecidas[i][j+1], '~w')
					self.removeIncerteza('wumpus?')

				elif 'visitada' in self.salasConhecidas[i-1][j]:
					adiciona(self.salasConhecidas[i][j+1], 'wumpus')
					adiciona(self.salasConhecidas[i-1][j], '~w')
					self.removeIncerteza('wumpus?')

			if diagonais[2] != 0 and 'fedor' in diagonais[2][2]:
				if 'visitada' in self.salasConhecidas[i][j-1]:
					adiciona(self.salasConhecidas[i+1][j], 'wumpus')
					adiciona(self.salasConhecidas[i][j-1], '~w')
					self.removeIncerteza('wumpus?')

				elif 'visitada' in self.salasConhecidas[i+1][j]:
					adiciona(self.salasConhecidas[i][j-1], 'wumpus')
					adiciona(self.salasConhecidas[i+1][j], '~w')
					self.removeIncerteza('wumpus?')

			if diagonais[3] != 0 and 'fedor' in diagonais[3][2]:
				if 'visitada' in self.salasConhecidas[i][j+1]:
					adiciona(self.salasConhecidas[i+1][j], 'wumpus')
					adiciona(self.salasConhecidas[i][j+1], '~w')
					self.removeIncerteza('wumpus?')

				elif 'visitada' in self.salasConhecidas[i+1][j]:
					adiciona(self.salasConhecidas[i][j+1], 'wumpus')
					adiciona(self.salasConhecidas[i+1][j], '~w')
					self.removeIncerteza('wumpus?')

		if status == 'brisa':

			if diagonais[0] != 0 and 'brisa' in diagonais[0][2]:
				if diagonais[2] != 0 and 'brisa' in diagonais[2][2]:
					adiciona(self.salasConhecidas[i][j-1], 'poço')
					remove(self.salasConhecidas[i][j-1], 'poço?')

				if diagonais[1] != 0 and 'brisa' in diagonais[1][2]:
					adiciona(self.salasConhecidas[i-1][j], 'poço')
					remove(self.salasConhecidas[i-1][j], 'poço?')

			if diagonais[3] != 0 and 'brisa' in diagonais[3][2]:
				if diagonais[1] != 0 and 'brisa' in diagonais[1][2]:
					adiciona(self.salasConhecidas[i][j+1], 'poço')
					remove(self.salasConhecidas[i][j+1], 'poço?')

				if diagonais[2] != 0 and 'brisa' in diagonais[2][2]:
					adiciona(self.salasConhecidas[i+1][j], 'poço')
					remove(self.salasConhecidas[i+1][j], 'poço?')

	# Função na qual o agente decide o que fazer: calcular caminho, movimentar, agarra o ouro, matar o wumpus, chutar...
	def acao (self):

		i = self.posicao[0]
		j = self.posicao[1]

		adiciona(self.salasConhecidas[i][j], 'visitada')

		sala = self.caverna[i][j]

		# Verifica os atributos na sala

		# A sala não tem nada
		if len(sala) == 0:
			adiciona(self.salasConhecidas[i][j], '~w')
			adiciona(self.salasConhecidas[i][j], '~p')
			remove(self.salasConhecidas[i][j], 'wumpus?')
			remove(self.salasConhecidas[i][j], 'poço?')
			self.inferirSalas('~w')
			self.inferirSalas('~p')

		elif 'poço' in sala or 'wumpus' in sala:
			
			self.status = 'Morreu!!'
			self.desempenho -= 1000

			self.salasConhecidas[self.posicao[0]][self.posicao[1]].remove('agente')
			self.caverna[self.posicao[0]][self.posicao[1]].remove('agente')

			thread.start_new_thread(soundFX, ('Audio/goofy_yell.mp3', False))

			if 'poço' in sala:
				adiciona(self.salasConhecidas[self.posicao[0]][self.posicao[1]], 'poço')
				remove(self.salasConhecidas[self.posicao[0]][self.posicao[1]], 'poço?')

			else:
				adiciona(self.salasConhecidas[self.posicao[0]][self.posicao[1]], 'wumpus')
				remove(self.salasConhecidas[self.posicao[0]][self.posicao[1]], 'wumpus?')

			return -1

		elif 'ouro' in sala:

			adiciona(self.salasConhecidas[i][j], 'ouro')
			self.agarrar()
			return 1

		# Se não achou o ouro e nem morreu, faz algumas inferências
		else:

			remove(self.salasConhecidas[i][j], 'wumpus?')
			remove(self.salasConhecidas[i][j], 'poço?')

			if 'fedor' in sala: # Infere possíveis localizações do Wumpus

				adiciona(self.salasConhecidas[i][j], 'fedor')
				adiciona(self.salasConhecidas[i][j], '~w')
				self.inferirSalas('wumpus?')
				self.infereDiagonais('fedor')

			else:
				adiciona(self.salasConhecidas[i][j], '~w')
				self.inferirSalas('~w')

			if 'brisa' in sala: # Infere possíveis localizações dos poços

				adiciona(self.salasConhecidas[i][j], 'brisa')
				adiciona(self.salasConhecidas[i][j], '~p')
				self.inferirSalas('poço?')
				self.infereDiagonais('brisa')

			else:
				adiciona(self.salasConhecidas[i][j], '~p')
				self.inferirSalas('~p')

		# Caso tenha percorrido todo o caminho calculado
		if self.indiceCaminho == len(self.caminho):

			# E não tenha que matar o Wumpus, calcula outro caminho
			if not self.matar:
				self.caminho = self.proximoPasso()
				self.indiceCaminho = 0
		
			# Se não, significa que precisa atirar no Wumpus
			else:
				self.atirar()
				self.matar = False

			# Se não houver nenhum caminho a ser seguido
			if self.caminho == -1:

				# E o agente tem munição, tentará matar o Wumpus
				if self.tiro:
					self.matar = True
					self.caminho = self.calculaCaminhoWumpus()

				# Do contrário, arriscará uma movimentação incerta
				else:
					self.status = 'Chutando!'
					self.caminho = self.calculaCaminhoChute()

		# Se o caminho ainda não acabou, continua percorrendo
		else:
			self.andar(self.caminho[self.indiceCaminho])

		return 0
				
	def imprimeCaverna (self):

		for i in range(0, 4):

			print(self.salasConhecidas[i], i)

		print ('')

# Funções de manipulação de listas

def adiciona (lista, elemento):
	if elemento not in lista:

		if elemento == 'wumpus': #Pequena trapacinha
			if 'wumpusmorto' not in lista:
				lista.append(elemento)

		else:
			lista.append(elemento)

def remove (lista, elemento):
	if elemento in lista:
		lista.remove(elemento)

def soundFX(arquivo, loop):

	if loop:
		while (True):
			playsound(arquivo)

	else:
		playsound (arquivo)