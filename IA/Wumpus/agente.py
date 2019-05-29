class Agente:

	def __init__ (self):

		self.flecha = True

		self.desempenho = 0

		self.salasConhecidas = [[[] for i in range(4)] for j in range(4)]

		self.posicao = (3, 0)

	def andar (self, direcao):

		print(direcao)

		i = self.posicao[0]
		j = self.posicao[1]

		if direcao == 'direita' and j < 3:
			self.posicao = (i, j+1)

		elif direcao == 'esquerda' and j > 0:
			self.posicao = (i, j-1)
	
		elif direcao == 'cima' and i > 0:
			self.posicao = (i-1, j)
	
		if direcao == 'baixo' and i < 3:
			self.posicao = (i+1, j)

		self.desempenho -= 1
