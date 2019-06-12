class Agente:

	def __init__ (self, caverna):

		self.resetaAgente(caverna)

	def resetaAgente (self, caverna):

		self.flecha = True

		self.desempenho = 0

		self.salasConhecidas = [[[] for i in range(4)] for j in range(4)]
		self.salasConhecidas[3][0].append('agente')
		
		self.caverna = caverna

		self.filaInferencias = []

		self.posicao = (3, 0)

		self.direcao = 'direita'

		self.status = 'Aguardando'

	def andar (self):

		print(self.direcao)

		i = self.posicao[0]
		j = self.posicao[1]

		if self.direcao == 'direita':
			if j < 3:
				self.posicao = (i, j+1)
			else:
				raise IndexError

		elif self.direcao == 'esquerda':
			if j > 0:
				self.posicao = (i, j-1)
			else:
				raise IndexError
	
		elif self.direcao == 'cima':
			if i > 0:
				self.posicao = (i-1, j)
			else:
				raise IndexError
	
		elif self.direcao == 'baixo':
			if i < 3:
				self.posicao = (i+1, j)
			else:
				raise IndexError

		self.salasConhecidas[i][j].remove('agente') 
		self.salasConhecidas[self.posicao[0]][self.posicao[1]].append('agente') 
		
		self.status = 'Andou'
		self.desempenho -= 1

	def virar (self, direcao):

		if direcao == 'direita':

			if self.direcao == 'direita':
				self.direcao = 'baixo'

			elif self.direcao == 'esquerda':
				self.direcao = 'cima'
		
			elif self.direcao == 'cima':
				self.direcao = 'direita'
		
			elif self.direcao == 'baixo':
				self.direcao = 'esquerda'

		elif direcao == 'esquerda':

			if self.direcao == 'direita':
				self.direcao = 'cima'

			elif self.direcao == 'esquerda':
				self.direcao = 'baixo'
		
			elif self.direcao == 'cima':
				self.direcao = 'esquerda'
		
			elif self.direcao == 'baixo':
				self.direcao = 'direita'

		self.desempenho -= 1
		self.status = 'Virou à ' + direcao

	def agarrar(self):

		self.desempenho += 1000
		self.status = 'Agarrou!'


	def acao (self):

		for atributo in self.caverna[self.posicao[0]][self.posicao[1]]:

			if atributo == 'ouro':

				self.salasConhecidas[self.posicao[0]][self.posicao[1]].append(atributo)
				self.agarrar()
				break

			elif atributo == 'fedor':

				self.salasConhecidas[self.posicao[0]][self.posicao[1]].append(atributo)

				if self.posicao[0] > 0:
					self.salasConhecidas[self.posicao[0]-1][self.posicao[1]].append('wumpus?')

				if self.posicao[0] < 3:
					self.salasConhecidas[self.posicao[0]+1][self.posicao[1]].append('wumpus?')
	
				if self.posicao[1] < 3:
					self.salasConhecidas[self.posicao[0]][self.posicao[1]+1].append('wumpus?')
	
				if self.posicao[1] > 0:
					self.salasConhecidas[self.posicao[0]][self.posicao[1]-1].append('wumpus?')

			elif atributo == 'brisa':

				self.salasConhecidas[self.posicao[0]][self.posicao[1]].append(atributo)

				if self.posicao[0] > 0:
					self.salasConhecidas[self.posicao[0]-1][self.posicao[1]].append('poço?')

				if self.posicao[0] < 3:
					self.salasConhecidas[self.posicao[0]+1][self.posicao[1]].append('poço?')
	
				if self.posicao[1] < 3:
					self.salasConhecidas[self.posicao[0]][self.posicao[1]+1].append('poço?')

				if self.posicao[1] > 0:
					self.salasConhecidas[self.posicao[0]][self.posicao[1]-1].append('poço?')


		try:
			self.andar()
			print ('ANDOU')

		except:
			self.virar('esquerda')
			print ('VIROU')
			print ('Nova direção: ' + self.direcao)
				
	def imprimeCaverna (self):

		for i in range(0, 4):

			print(self.salasConhecidas[i], i)

		print ('')