import random
class Caverna:

	def __init__ (self, posicaoAgente):

		self.geraCaverna(posicaoAgente)

	def geraCaverna (self, posicaoAgente):

		self.salas = [[[] for i in range(4)] for j in range(4)]

		self.posicaoAgente = posicaoAgente

		self.salas[posicaoAgente[0]][posicaoAgente[1]].append('agente')

		i = random.randint(0, 3)
		if i == 3:
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

		# for i in range(0, 4):
		# 	for j in range(0, 4):

		# 		if self.salas[i][j] == []:
		# 			self.salas[i][j].append('nada')

	def imprimeCaverna (self):

		for i in range(0, 4):

			print(self.salas[i], i)

		print ('')

	def atualizaAgente (self, posicaoAgente):

		self.salas[self.posicaoAgente[0]][self.posicaoAgente[1]].remove('agente')
		
		# if self.salas[self.posicaoAgente[0]][self.posicaoAgente[1]] == []:
		# 	self.salas[posicaoAgente[0]][posicaoAgente[1]].append('nada')

		self.salas[posicaoAgente[0]][posicaoAgente[1]].append('agente')
		self.posicaoAgente = posicaoAgente