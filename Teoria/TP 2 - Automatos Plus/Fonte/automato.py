from entrada_saida import *
from graphviz import Digraph
from queue import Queue
from misc import Any

class Automato:

	def __init__ (self): # Construtor
		
		self.tipo = None
		self.descricao = "Autômato sem descrição"
		self.alfabeto = []
		self.alfabetoPilha = []
		self.transicoes = {}
		self.estadosAtivos = {}
		self.estadoInicial = None
		self.estadosFinais = []
		self.grafo = Digraph(format='svg')

	# Recebe o edereço da entrada, constrói o grafo do autômato e salva com o nome apropriado
	def montaGrafo (self, arquivo):
		
		self.arquivo = arquivo

		self.grafo.attr(rankdir='LR')
		self.grafo.attr('edge', arrowsize="0.3")

		# Um nó invisível, utilizado para criar a seta do estado inicial
		self.grafo.node('', shape='plaintext', fixedsize='true', height='0.1', width='0.1')

		for no in self.transicoes.keys(): # Para cada estado, cria um nó no grafo

			if no in self.estadosFinais: # Caso o estado seja final, círculo duplo

				self.grafo.attr('node', shape='doublecircle')

			else:

				self.grafo.attr('node', shape='circle')

			self.grafo.node(no)

		arestas = {}

		for no in self.transicoes.keys(): # Para cada transição, cria uma aresta no grafo

			if no == self.estadoInicial: # Cria a seta do estado inicial

				self.grafo.edge('', no, arrowsize='0.5')

			for transicao in self.transicoes[no]:

				for no2 in self.transicoes[no][transicao]:

					if (no+' '+no2) in arestas.keys():
						arestas[no+' '+no2] = arestas[no+' '+no2] + ", " + transicao

					else:
						arestas[no+' '+no2] = transicao

		for aresta in arestas.keys():

			self.grafo.edge(aresta.split(' ')[0], aresta.split(' ')[1], label=arestas[aresta])
			
		# Salva o grafo num arquivo svg, pasta "Grafos"
		self.grafo.render(filename=(arquivo.replace("Entradas", "Grafos")), format='svg', cleanup=True)

	# Devolve um grafo ressaltando os estados ativos de palavra ao processar indice
	def montaGrafoPassoAPasso (self, palavra, indice):

		grafo = Digraph()
		grafo.attr(rankdir='LR')
		# automato.grafo.node(automato.estadoInicial)

		grafo.node('', shape='plaintext', fixedsize='true', height='0.1', width='0.1')

		# Para cada no, decide se ressalta ou não
		for no in self.transicoes.keys():

			if no in self.estadosFinais:
				grafo.attr('node', shape='doublecircle')

			else:
				grafo.attr('node', shape='circle')

			# Caso antes do processamento da palavra
			if indice == -1:

				# O estado inicial se ativa
				if no == self.estadoInicial:
					grafo.attr('node', color='red')

				else:
					grafo.attr('node', color='black')

			# Caso contrário
			else:

				# Se o nó estiver aivo, é colorido de vermelho
				if no in self.estadosAtivos[indice]:
					grafo.attr('node', color='red')

				else:
					grafo.attr('node', color='black')

			grafo.node(no)

		# Dicionário auxiliar para evitar transições desnecessárias
		# i.e., ao caso haja mais de uma transição saindo do nó a e levando ao no b, elas são
		# condensadas na mesma transição
		arestas = {}

		# Para cada transição, condensa as transições desnecessárias
		for no in self.transicoes.keys():

			for transicao in self.transicoes[no]:

				for no2 in self.transicoes[no][transicao]:

					if (no+' '+no2) in arestas.keys():
						arestas[no+' '+no2].append(transicao)

					else:
						arestas[no+' '+no2] = [transicao]

		# Para cada transição, decide se ressalta ou não
		for aresta in arestas.keys():

			no = aresta.split(' ')
			no2 = no[1]
			no = no[0]

			if indice > 0 and palavra[indice] in arestas[aresta] and no2 in self.estadosAtivos[indice] and no in self.estadosAtivos[indice-1]:
				grafo.attr('edge', color='red')

			elif indice == 0 and palavra[indice] in arestas[aresta] and no == self.estadoInicial:
				grafo.attr('edge', color='red')

			else:
				grafo.attr('edge', color='black')

			grafo.edge(no, no2, label=(((str(arestas[aresta])).replace("'", '')).replace(']', '')).replace('[', ''))

		return grafo

	def destroiAutomato (self): # Reseta todos os dados do autômato

		self.arquivo = None
		self.tipo = None
		self.descricao = "Autômato sem descrição"
		self.alfabeto.clear()
		self.alfabetoPilha.clear()
		self.transicoes.clear()
		self.estadosAtivos.clear()
		self.estadoInicial = None
		self.estadosFinais.clear()
		self.grafo.clear(keep_attrs=False)

	# Recebe uma palavra e verifica se e quais símbolos não são aceitos pelo alfabeto do autômato
	def verificaAlfabeto (self, palavra):

		caracteres = [] # Armazena os símbolos não aceitos

		for c in palavra:

			if c not in self.alfabeto and c not in caracteres:

				caracteres.append(c)

		if len(caracteres) > 0:

			return "Palavra não aceita! - Os símbolos " + str(caracteres)\
			+ " não estão no alfabeto\n<< Alfabeto: " + str(self.alfabeto)

		return True

	# Recebe uma palavra a ser testada e um dicionário onde poderá ser salvo o passo-a-passo
	def testaPalavra (self, palavra, passoAPasso):

		if palavra == '': # Caso a palavra seja vazia

			if self.estadoInicial in self.estadosFinais:
				retorno = "Palavra aceita!"
		
			else:
				retorno = "Palavra não aceita!"

		else:

			# Verifica se a palavra é aceita pelo alfabeto do autômato
			retorno = self.verificaAlfabeto(palavra)

		if retorno == True: # Caso seja, testa as transições

			# Índices da palavra
			caractere = 0
			caractereAnterior = 0

			# A busca começa no estado inicial e tenta alcançar o estado final
			estadoAtual = self.estadoInicial

			# A pilha armazena duplas do tipo (estado, indice da palavra a ser processado no estado)
			fila = Queue()
			fila.put([estadoAtual, caractere])

			# Caso o usuário queira exibir o passo-a-passo, limpa o dicionário de estados,
			# pois ele será diferente para cada palavra
			if passoAPasso:

				self.estadosAtivos.clear()

			while True:
	
				# Se a pilha não estiver vazia, desempílha uma dupla e processa a transição a partir do estado
				if not fila.empty(): 

					aux = fila.get()
					estadoAtual = aux[0] # Novo estado atual
					caractere = aux[1] # Indice da palavra que armazena o caractere a ser processado

				# Se a pilha estiver vazia, significa que, ao final do processamento,
				# nenhum estado final foi atingido
				else:

					retorno = "Palavra não aceita!"

					break

				# Se o índice a ser processado for -1, significa que o autômato chegou
				# ao fim de um dos caminhos de processamento da palavra
				if caractere == -1:

					# Dessa forma, se o estado atual for final, a palavra deve ser aceita
					if estadoAtual in self.estadosFinais:

						retorno = "Palavra aceita!"
						
						break

				# Do contrário, processa a transição a prtir do estado atual
				else:

					# Caso a transição exista na tabela de transições
					if palavra[caractere] in self.transicoes[estadoAtual].keys():
						
						# O passo-a-passo funciona armazenando em um dicionário todos os estados
						# ativos ao processar cada símbolo da palavra
						if passoAPasso:

							if caractere not in self.estadosAtivos.keys():

								self.estadosAtivos[caractere] = []
						
						# Para todos os estados atingidos a partir da transição
						for estado in self.transicoes[estadoAtual][palavra[caractere]]:

							# Caso o caminho de processamento não tenha terminado, empilha o estado
							# e o próximo índice da palavra a ser processado
							if caractere + 1 != len(palavra):
								fila.put([estado, caractere+1])

							# Caso o índice da palavra seja o último, fim de um caminho de processamento
							else:
								fila.put([estado, -1])

							# Armazena o estado no dicionário de passo-a-passo
							if passoAPasso and estado not in self.estadosAtivos[caractere]:
								self.estadosAtivos[caractere].append(estado)

		return retorno

	def testaPalavraPilha (self, palavra, passoAPasso):

		if palavra == '': # Caso a palavra seja vazia

			if self.estadoInicial in self.estadosFinais:
				retorno = "Palavra aceita!"
		
			else:
				retorno = "Palavra não aceita!"

		else:

			# Verifica se a palavra é aceita pelo alfabeto do autômato
			retorno = self.verificaAlfabeto(palavra)

		if retorno == True: # Caso seja, testa as transições

			# Índices da palavra
			caractere = 0
			caractereAnterior = 0

			# A busca começa no estado inicial e tenta alcançar o estado final
			estadoAtual = self.estadoInicial

			# A fila armazena duplas do tipo (estado, indice da palavra a ser processado no estado)
			fila = [[estadoAtual, caractere]]

			# A pilha do autômato começa vazia
			pilha = []

			# Variável usada como tipo 'coringa'
			ANYTHING = Any()

			# Caso o usuário queira exibir o passo-a-passo, limpa o dicionário de estados,
			# pois ele será diferente para cada palavra
			if passoAPasso:

				self.estadosAtivos.clear()

			while True:
	
				# Se a fila não estiver vazia, desempílha uma dupla e processa a transição a partir do estado
				if len(fila) > 0: 

					aux = fila.pop(0)
					estadoAtual = aux[0] # Novo estado atual
					caractere = aux[1] # Indice da palavra que armazena o caractere a ser processado

				# Se a pilha estiver vazia, significa que, ao final do processamento,
				# nenhum estado final foi atingido
				else:

					retorno = "Palavra não aceita!"

					break

				# Se o índice a ser processado for -1, significa que o autômato chegou
				# ao fim de um dos caminhos de processamento da palavra
				if caractere == -1:

					# Dessa forma, se o estado atual for final, a palavra deve ser aceita
					if estadoAtual in self.estadosFinais:

						retorno = "Palavra aceita!"
						
						break

				# Do contrário, processa a transição a prtir do estado atual
				else:

					# Processa as transições vazias
					self.transicoesVazias(fila, estadoAtual, caractere)
					print(fila)
					#input()

					# Processa as transições interrogativas
					self.transicoesInterrogativas(fila, estadoAtual, caractere, palavra, pilha)

					# Processa a transição
					for transicao in self.transicoes[estadoAtual].keys():

						# Caso a transição exista na tabela de transições
						if transicao[0] == palavra[caractere]:

							# O passo-a-passo funciona armazenando em um dicionário todos os estados
							# ativos ao processar cada símbolo da palavra
							if passoAPasso:

								if caractere not in self.estadosAtivos.keys():

									self.estadosAtivos[caractere] = []

							# Para todos os estados atingidos a partir da transição
							for estado in self.transicoes[estadoAtual][transicao]:

								print(estadoAtual, estado)

								desempilha = transicao[1]
								empilha = transicao[2]

								try:
									if desempilha != '&' and desempilha != '?':
										pilha.reverse()
										pilha.remove(desempilha)
										pilha.reverse()

								except:
									pass

								else:
									# Caso o caminho de processamento não tenha terminado, empilha o estado
									# e o próximo índice da palavra a ser processado
									if caractere + 1 != len(palavra):
										fila.append([estado, caractere+1])

									# Caso o índice da palavra seja o último, fim de um caminho de processamento
									else:
										fila.append([estado, -1])

									# Armazena o estado no dicionário de passo-a-passo
									if passoAPasso and estado not in self.estadosAtivos[caractere]:
										self.estadosAtivos[caractere].append(estado)

									if empilha != '&' and empilha != '?':
										pilha.append(empilha)

		return retorno

	def transicoesVazias (self, fila, estado, caractere):

		filaTemp = [estado]
		transVazia = ('&', '&', '&')

		while len(filaTemp) > 0:

			atual = filaTemp.pop(0)

			if transVazia in self.transicoes[atual]:
	
				for e in self.transicoes[atual][transVazia]:

					filaTemp.append(e)
					fila.append([e, caractere])

	def transicoesInterrogativas (self, fila, estado, caractere, palavra, pilha):

		for transicao in self.transicoes[estado]:

			if transicao[0] == '?':

				if transicao[1] == '?':

					if caractere == len(palavra)-1 and len(pilha) == 0:
						for e in self.transicoes[estado][transicao]:
							fila.append([e, -1])

				else:
					if caractere == len(palavra)-1:
						for e in self.transicoes[estado][transicao]:
							fila.append([e, -1])

			elif transicao[1] == '?':

				for e in self.transicoes[estado][transicao]:
					
					if caractere == len(palavra)-1:
						fila.append([e, -1])

					else:
						fila.append([e, caractere+1])

	# Imprime o dicionário de passo-a-passo
	def imprimePassoAPasso (self, palavra):

		print ("<< Estado inicial: " + (self.estadoInicial.replace('*', '')).replace('+', ''))

		for indice in self.estadosAtivos.keys():

			print ("<< Simbolo: " + palavra[indice] + " - Estados ativos: " + str(self.estadosAtivos[indice]))
