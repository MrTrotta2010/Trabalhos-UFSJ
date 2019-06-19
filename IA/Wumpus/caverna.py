import random

class Caverna:

	def __init__ (self, posicaoAgente, debug):

		self.geraCaverna(posicaoAgente, debug)

	def geraCaverna (self, posicaoAgente, debug):

		self.salas = [[[] for i in range(4)] for j in range(4)]

		self.posicaoAgente = posicaoAgente

		self.salas[posicaoAgente[0]][posicaoAgente[1]].append('agente')

		if debug == '0':

			i = random.randint(0, 3)
			if i == 3:
				j = random.randint(2, 3)
			elif i == 2:
				j = random.randint(1, 3)
			else:
				j = random.randint(0, 3)

			self.salas[i][j].append('wumpus')

			if i > 0:
				self.salas[i-1][j].append('fedor')

			if i < 3:
				self.salas[i+1][j].append('fedor')
			
			if j > 0:
				self.salas[i][j-1].append('fedor')
			
			if j < 3:
				self.salas[i][j+1].append('fedor')

			i = random.randint(0, 3)
			if i == 3:
				j = random.randint(1, 3)
			else:
				j = random.randint(0, 3)

			self.salas[i][j].append('ouro')

			for i in range(0, 4):
				for j in range(0, 4):

					if (i != 2 and j != 0) and (i != 3 and j != 1):
					
						if random.randint(0, 101) < 20:

							if 'wumpus' not in self.salas[i][j] and 'ouro' not in self.salas[i][j] and 'agente' not in self.salas[i][j]:
								self.salas[i][j].append('poço')
									
								if i > 0:
									self.salas[i-1][j].append('brisa')

								if i < 3:
									self.salas[i+1][j].append('brisa')
								
								if j > 0:
									self.salas[i][j-1].append('brisa')
								
								if j < 3:
									self.salas[i][j+1].append('brisa')

		# Abaixo estão alguns mapas de debug, com casos especiais de execução

		# Agente mata o Wumpus e pega o ouro
		elif debug == '1':
			self.salas[0][3].append('wumpus')
			self.salas[0][3].append('ouro')
			self.salas[1][3].append('fedor')
			self.salas[0][2].append('fedor')

		# Agente mata o Wumpus e pega o ouro desviando de poços
		elif debug == '2':
			self.salas[0][2].append('wumpus')
			self.salas[0][2].append('ouro')
			self.salas[1][2].append('fedor')
			self.salas[0][1].append('fedor')
			self.salas[0][3].append('fedor')
			self.salas[1][2].append('poço')
			self.salas[0][2].append('brisa')
			self.salas[2][2].append('brisa')
			self.salas[1][1].append('brisa')
			self.salas[1][3].append('brisa')

		# Agente mata o Wumpus para evitar poços
		elif debug == '3':
			self.salas[3][3].append('wumpus')
			self.salas[3][2].append('fedor')
			self.salas[2][3].append('fedor')
			self.salas[1][3].append('ouro')
			self.salas[0][2].append('poço')
			self.salas[1][2].append('poço')
			self.salas[0][2].append('brisa')
			self.salas[2][2].append('brisa')
			self.salas[0][1].append('brisa')
			self.salas[1][1].append('brisa')
			self.salas[2][2].append('brisa')
			self.salas[0][3].append('brisa')
			self.salas[1][3].append('brisa')

		# Agente chuta uma movimentação e evita um poço
		elif debug == '4':
			self.salas[3][3].append('wumpus')
			self.salas[3][2].append('fedor')
			self.salas[2][3].append('fedor')
			self.salas[0][3].append('ouro')
			self.salas[1][2].append('poço')
			self.salas[0][2].append('brisa')
			self.salas[2][2].append('brisa')
			self.salas[1][1].append('brisa')
			self.salas[1][3].append('brisa')

		# Agente chuta uma movimentação mas cai no poço
		elif debug == '5':
			self.salas[2][3].append('wumpus')
			self.salas[1][3].append('fedor')
			self.salas[2][2].append('fedor')
			self.salas[3][3].append('fedor')
			self.salas[0][3].append('ouro')
			self.salas[0][2].append('poço')
			self.salas[1][3].append('poço')
			self.salas[0][1].append('brisa')
			self.salas[0][3].append('brisa')
			self.salas[1][2].append('brisa')
			self.salas[2][3].append('brisa')

	def imprimeCaverna (self):

		for i in range(0, 4):

			print(self.salas[i], i)

		print ('')

	def atualizaAgente (self, posicaoAgente):

		try:
			self.salas[posicaoAgente[0]][posicaoAgente[1]].append('agente')
		
		except IndexError:
			pass

		else:
			self.salas[self.posicaoAgente[0]][self.posicaoAgente[1]].remove('agente')
			self.posicaoAgente = posicaoAgente