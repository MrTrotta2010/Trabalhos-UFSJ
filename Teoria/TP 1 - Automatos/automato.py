from entrada_saida import *
from graphviz import Digraph

class Automato:

	def __init__ (self): # Construtor
		
		self.tipo = None
		self.descricao = None
		self.alfabeto = []
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

		for no in self.transicoes.keys(): # Para cada transição, cria uma aresta no grafo

			if no == self.estadoInicial: # Cria a seta do estado inicial

				self.grafo.edge('', no, arrowsize='0.5')

			for transicao in self.transicoes[no]:

				for no2 in self.transicoes[no][transicao]:

					self.grafo.edge(no, no2, label=transicao)

		# Salva o grafo num arquivo svg, pasta "Grafos"
		self.grafo.render(filename=(arquivo.replace("Entradas", "Grafos")), format='svg', cleanup=True)

	def destroiAutomato (self): # Reseta todos os dados do autômato

		self.arquivo = None
		self.tipo = None
		self.descricao = None
		self.alfabeto.clear()
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
			pilha = []
			pilha.append([estadoAtual, caractere])

			# Caso o usuário queira exibir o passo-a-passo, limpa o dicionário de estados,
			# pois ele será diferente para cada palavra
			if passoAPasso:

				self.estadosAtivos.clear()

			while True:
	
				# Se a pilha não estiver vazia, desempílha uma dupla e processa a transição a partir do estado
				if len(pilha) > 0: 

					aux = pilha.pop()
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
						if passoAPasso and caractere != -1:

							if caractere not in self.estadosAtivos.keys():

								self.estadosAtivos[caractere] = []
						
						# Para todos os estados atingidos a partir da transição
						for estado in self.transicoes[estadoAtual][palavra[caractere]]:

							# Caso o caminho de processamento não tenha terminado, empilha o estado
							# e o próximo índice da palavra a ser processado
							if caractere + 1 != len(palavra):
								pilha.append([estado, caractere+1])

							# Caso o índice da palavra seja o último, fim de um caminho de processamento
							else:
								pilha.append([estado, -1])

							# Armazena o estado no dicionário de passo-a-passo
							if passoAPasso and caractere != -1 and (estado not in self.estadosAtivos[caractere]):
								self.estadosAtivos[caractere].append((estado.replace('*', '')).replace('+', ''))

		return retorno

	# Imprime o dicionário de passo-a-passo
	def imprimePassoAPasso (self, palavra):

		print ("<< Estado inicial: " + (self.estadoInicial.replace('*', '')).replace('+', ''))

		for indice in self.estadosAtivos.keys():

			print ("<< Simbolo: " + palavra[indice] + " - Estados ativos: " + str(self.estadosAtivos[indice]))