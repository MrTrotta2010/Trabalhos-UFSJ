from queue import Queue

class Agente:

	def __init__ (self, caverna):

		self.resetaAgente(caverna)

	def resetaAgente (self, caverna):

		self.flecha = True

		self.desempenho = 0

		self.salasConhecidas = [[[] for i in range(4)] for j in range(4)]
		self.salasConhecidas[3][0].append('agente')
		
		self.caverna = caverna
		# self.visitados = [][]

		self.filaInferencias = []

		self.posicao = (3, 0)

		self.direcao = 'direita'

		self.status = 'Aguardando'

		self.achouWumpus = False

		self.caminho = []
		self.indiceCaminho = 0

	def ordenaCustos (self, destinos):

		custos = []
		i = 0

		for sala in destinos:

			custos.append(0)

			print('Posições: ', sala, self.posicao)

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

		print('Custos: ', custos)

		print('destinos antes : ', destinos)
		return [x for _,x in sorted(zip(custos, destinos))], sorted(custos)
		#print('destinos depois: ', destinos)

	def calculaCusto (self, caminhos, destino):

		custo = 0

		atual = destino

		while atual != (self.posicao[0], self.posicao[1], self.direcao):

			custo += 1

			print('atual: ', atual)
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

	def calculaCaminho (self, caminhos, destino):

		atual = destino
		caminho = []
		print ('!!!!!!!', atual)

		while atual != (self.posicao[0], self.posicao[1], self.direcao):

			caminho.append((atual[0], atual[1], atual[2]))
			atual = caminhos[atual]

		caminho.reverse()

		return caminho

	# def proximoPasso(self):

	# 	i = self.posicao[0]
	# 	j = self.posicao[1]

	# 	destinos = []
	# 	print("proximo")

	# 	if i > 0:
	# 		destinos.append((i-1, j, 'cima'))
		
	# 	if i < 3:
	# 		destinos.append((i+1, j, 'baixo'))
		
	# 	if j > 0:
	# 		destinos.append((i, j-1, 'esquerda'))
		
	# 	if j < 3:
	# 		destinos.append((i, j+1, 'direita'))

	# 	destinos, custos = self.ordenaCustos(destinos)
	# 	print('destinos depois', destinos, custos)

	# 	destino = -1

	# 	for d in range(len(destinos)):

	# 		i = destinos[d][0]
	# 		j = destinos[d][1]
	# 		print('i j', i, j)

	# 		if 'visitada' not in self.salasConhecidas[i][j]:

	# 			if '~w' in self.salasConhecidas[i][j] and '~p' in self.salasConhecidas[i][j]:
	# 				destino = d
	# 				break

	# 		else:
	# 			if destino == -1:
	# 				destino = d

	# 	print('Vai andar para ', destinos[destino])

	# 	return destinos[destino], custos[destino]

	def buscaLargura (self):

		i = self.posicao[0]
		j = self.posicao[1]

		borda = Queue()
		destinos= []
		vertices = {} # sala : pai

		borda.put((i, j, self.direcao))

		while not borda.empty():

			sala = borda.get()

			if sala[0] > 0:
				if (sala[0]-1, sala[1]) not in vertices.keys():
					vertices[(sala[0]-1, sala[1], 'cima')] = (sala[0], sala[1], sala[2])
			
				if 'visitada' in self.salasConhecidas[sala[0]-1][sala[1]]:
					borda.put((sala[0]-1, sala[1], 'cima'))
					print('1')

				elif '~w' in self.salasConhecidas[sala[0]-1][sala[1]] and '~p' in self.salasConhecidas[sala[0]-1][sala[1]]:
					destinos.append((sala[0]-1, sala[1], 'cima'))

			if sala[0] < 3:
				if (sala[0]+1, sala[1]) not in vertices.keys():
					vertices[(sala[0]+1, sala[1], 'baixo')] = (sala[0], sala[1], sala[2])

				if 'visitada' in self.salasConhecidas[sala[0]+1][sala[1]]:
					borda.put((sala[0]+1, sala[1], 'baixo'))
					print('2')

				elif '~w' in self.salasConhecidas[sala[0]+1][sala[1]] and '~p' in self.salasConhecidas[sala[0]+1][sala[1]]:
					destinos.append((sala[0]+1, sala[1], 'baixo'))
			
			if sala[1] > 0:
				if (sala[0], sala[1]-1) not in vertices.keys():
					vertices[(sala[0], sala[1]-1, 'esquerda')] = (sala[0], sala[1], sala[2])

				if 'visitada' in self.salasConhecidas[sala[0]][sala[1]-1]:
					borda.put((sala[0], sala[1]-1, 'esquerda'))
					print('3')

				elif '~w' in self.salasConhecidas[sala[0]][sala[1]-1] and '~p' in self.salasConhecidas[sala[0]][sala[1]-1]:
					destinos.append((sala[0], sala[1]-1, 'esquerda'))
			
			if sala[1] < 3:
				if (sala[0], sala[1]+1) not in vertices.keys():
					vertices[(sala[0], sala[1]+1, 'direita')] = (sala[0], sala[1], sala[2])

				if 'visitada' in self.salasConhecidas[sala[0]][sala[1]+1]:
					borda.put((sala[0], sala[1]+1, 'direita'))
					print('4')

				elif '~w' in self.salasConhecidas[sala[0]][sala[1]+1] and '~p' in self.salasConhecidas[sala[0]][sala[1]+1]:
					destinos.append((sala[0], sala[1]+1, 'direita'))

			# if len(destinos) > 0:
			# 	break

		print('vértices\n', vertices)
		print('destinos\n', destinos)

		return vertices, destinos

	def proximoPasso(self):

		i = self.posicao[0]
		j = self.posicao[1]

		caminhos, destinos = self.buscaLargura()

		custos = []

		for sala in destinos:

			custos.append(self.calculaCusto(caminhos, sala))

		print ('Custos ', custos)

		destino = [x for _,x in sorted(zip(custos, destinos))][0]

		print ('Destino ', destino)

		return self.calculaCaminho(caminhos, destino)

	# def andar (self):

	# 	print(self.direcao)

	# 	i = self.posicao[0]
	# 	j = self.posicao[1]

	# 	destino, custo = self.proximoPasso()

	# 	self.posicao = (destino[0], destino[1])

	# 	self.virar(destino[2], custo)

	# 	self.salasConhecidas[i][j].remove('agente') 
	# 	self.salasConhecidas[self.posicao[0]][self.posicao[1]].append('agente') 
		
	# 	self.status = 'Andou'
	# 	self.desempenho -= 1

	def andar (self, destino):

		print ('Destino ', destino)

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

		self.posicao = (destino[0], destino[1], destino[2])
		self.direcao = destino[2]
		self.desempenho -= custo
		self.indiceCaminho += 1

		self.salasConhecidas[self.posicao[0]][self.posicao[1]].append('agente')
		
	def virar (self, direcao, custo):

		self.direcao = direcao

		self.desempenho -= custo
		self.status = 'Virou para' + direcao

	def agarrar(self):

		self.desempenho += 1000
		self.status = 'Agarrou!'

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

	def infereDiagonais (self, status):

		i = self.posicao[0]
		j = self.posicao[1]

		diagonais = [0, 0, 0, 0]

		#cima esquerda
		try:
			diagonais[0] = (i-1, j-1, self.salasConhecidas[i-1][j-1])
		except:
			pass

		#cima direita
		try:
			diagonais[1] = (i-1, j+1, self.salasConhecidas[i-1][j+1])
		except:
			pass

		#baixo esquerda
		try:
			diagonais[2] = (i+1, j-1, self.salasConhecidas[i+1][j-1])
		except:
			pass

		#baixo direita
		try:
			diagonais[3] = (i+1, j+1, self.salasConhecidas[i+1][j+1])
		except:
			pass

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

	def acao (self):

		print("POSIÇÃO 0 ",self.posicao[0])
		print("POSIÇÃO 1 ",self.posicao[1])

		i = self.posicao[0]
		j = self.posicao[1]

		adiciona(self.salasConhecidas[i][j], 'visitada')

		sala = self.caverna[i][j]

		if len(sala) == 0:
			print("NADA")
			adiciona(self.salasConhecidas[i][j], '~w')
			adiciona(self.salasConhecidas[i][j], '~p')
			self.inferirSalas('~w')
			self.inferirSalas('~p')

		elif 'poço' in sala or 'wumpus' in sala:
			
			print("MORREU")
			return None, -1


		elif 'ouro' in sala:

			print("OURO")
			adiciona(self.salasConhecidas[i][j], 'ouro')
			self.agarrar()
			return None, 1

		else:

			if 'fedor' in sala:

				print("FEDOR")
				adiciona(self.salasConhecidas[i][j], 'fedor')
				adiciona(self.salasConhecidas[i][j], '~w')
				self.inferirSalas('wumpus?')
				self.infereDiagonais('fedor')

			else:
				adiciona(self.salasConhecidas[i][j], '~w')
				self.inferirSalas('~w')

			if 'brisa' in sala:

				print("brisa")
				adiciona(self.salasConhecidas[i][j], 'brisa')
				adiciona(self.salasConhecidas[i][j], '~p')
				self.inferirSalas('poço?')
				self.infereDiagonais('brisa')

			else:
				adiciona(self.salasConhecidas[i][j], '~p')
				self.inferirSalas('~p')

			# self.salasConhecidas[self.posicao[0]][self.posicao[1]].append('nada')

		if self.indiceCaminho == len(self.caminho):
			self.caminho = self.proximoPasso()
			self.indiceCaminho = 0
			print('Caminho', self.caminho)

		else:
			print('self.caminho ', self.caminho)
			self.andar(self.caminho[self.indiceCaminho])
			print ('ANDOU')

		return 0
				
	def imprimeCaverna (self):

		for i in range(0, 4):

			print(self.salasConhecidas[i], i)

		print ('')

	def removeIncerteza(self, status):

		for i in range(4):
			for j in range(4):
				if status in self.salasConhecidas[i][j]:
					self.salasConhecidas[i][j].remove(status)

				if status == 'wumpus?' and 'wumpus' not in self.salasConhecidas[i][j]:
					self.achouWumpus = True
					adiciona(self.salasConhecidas[i][j], '~w')

def adiciona (lista, elemento):
	if elemento not in lista:
		lista.append(elemento)

def remove (lista, elemento):
	if elemento in lista:
		lista.remove(elemento)