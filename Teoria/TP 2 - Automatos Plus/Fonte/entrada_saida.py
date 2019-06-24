import sys
import automato

# Trata os argumentos passados na execução do programa
def pegaArqEntrada (argumentos):

	if len(argumentos) == 2:

		return argumentos[1]

	return ""

def pegaTipo (tipo): # Devolve o tipo do automato

	if tipo == 'AFD':

		return 1

	elif tipo == 'AFN':

		return 2

	elif tipo == 'APD':

		return 3

	elif tipo == 'APN':

		return 4

	return -1

def constroiAutomatoFinito (linha, aut, cont):

	linha = linha.replace('\n', "")
	valores = linha.split('-')

	# Verifica para os dois estados da transição
	for estado in [valores[0], valores[2]]:

		# Caso o estado venha acompanhado de '+', é o estado inicial
		if estado[0] == '+':

			# Só pode haver um estado inicial
			if aut.estadoInicial == None or aut.estadoInicial == estado:

				aut.estadoInicial = estado

				# Caso também venha acompanhado de '*', também é final
				if estado[1] == '*':

					if estado not in aut.estadosFinais:

						aut.estadosFinais.append((estado.replace("+", "")).replace("*", ""))

				elif estado[1] == '+':

					arq.close()
					return "ERRO - A opção '++' não é válida para os estados!"		

			else:

				arq.close()
				return "ERRO - O autômato possui mais de um estado inicial!"
		
		# Caso o estado venha companhado de '*', é final		
		elif estado[0] == '*':

			if estado not in aut.estadosFinais:

				aut.estadosFinais.append((estado.replace("+", "")).replace("*", ""))

				if estado[1] == '*':

					arq.close()
					return "ERRO - A opção '**' não é válida para os estados!"
												
				elif estado[1] == '+':

					arq.close()
					return "ERRO - A opção '*+' não é válida para os estados!"

	# Formata os nomes dos estados
	estado1 = (valores[0].replace("+", "")).replace("*", "")
	estado2 = (valores[2].replace("+", "")).replace("*", "")

	# Adiciona os estados e transições à tabela de transições
	if estado1 not in aut.transicoes.keys():

		aut.transicoes[estado1] = {}

	if estado2 not in aut.transicoes.keys():

		aut.transicoes[estado2] = {}

	if valores[1] not in aut.alfabeto:

		return "ERRO - A transição não está no alfabeto - Linha " + str(cont+1) + ": " + linha

	if valores[1] not in aut.transicoes[estado1].keys():

		aut.transicoes[estado1][valores[1]] = []

	if estado2 in aut.transicoes[estado1][valores[1]]:

		arq.close()
		return "ERRO - Transição repetida! - Linha " + str(cont+1) + ": " + linha

	aut.transicoes[estado1][valores[1]].append(estado2)

	# Caso o autômato seja AFD mas tenha alguma transição que leva a um conjunto de estados
	if aut.tipo == 1 and len(aut.transicoes[estado1][valores[1]]) != 1:

		arq.close()
		return ("ERRO - O autômato é AFD mas tem transição não determinista! - "+estado1+"-"+valores[1]+"-"
			+str(aut.transicoes[estado1][valores[1]]))

	return None

def constroiAutomatoPilha (linha, aut, cont):

	linha = linha.replace('\n', "")
	valores = linha.split('-')

	# Verifica para os dois estados da transição
	for estado in [valores[0], valores[2]]:

		# Caso o estado venha acompanhado de '+', é o estado inicial
		if estado[0] == '+':

			# Só pode haver um estado inicial
			if aut.estadoInicial == None or aut.estadoInicial == estado:

				aut.estadoInicial = estado

				# Caso também venha acompanhado de '*', também é final
				if estado[1] == '*':

					if estado not in aut.estadosFinais:

						aut.estadosFinais.append((estado.replace("+", "")).replace("*", ""))

				elif estado[1] == '+':

					arq.close()
					return "ERRO - A opção '++' não é válida para os estados!"		

			else:

				arq.close()
				return "ERRO - O autômato possui mais de um estado inicial!"
		
		# Caso o estado venha companhado de '*', é final		
		elif estado[0] == '*':

			if estado not in aut.estadosFinais:

				aut.estadosFinais.append((estado.replace("+", "")).replace("*", ""))

				if estado[1] == '*':

					arq.close()
					return "ERRO - A opção '**' não é válida para os estados!"
												
				elif estado[1] == '+':

					arq.close()
					return "ERRO - A opção '*+' não é válida para os estados!"

	# Formata os nomes dos estados
	estado1 = (valores[0].replace("+", "")).replace("*", "")
	estado2 = (valores[2].replace("+", "")).replace("*", "")

	# Adiciona os estados e transições à tabela de transições
	if estado1 not in aut.transicoes.keys():

		aut.transicoes[estado1] = {}

	if estado2 not in aut.transicoes.keys():

		aut.transicoes[estado2] = {}

	transicao = valores[1].replace('(', '')
	transicao = transicao.replace(')', '')
	transicao = transicao.split(',')

	if len(transicao) > 3:
		return "ERRO - A transição tem parâmetros em excesso! - Linha " + str(cont+1) + ": " + linha

	elif len(transicao) < 3:
		return "ERRO - Faltam parâmetros na transição! - Linha " + str(cont+1) + ": " + linha

	if transicao[0] != '&' and transicao[0] != '?' and transicao[0] not in aut.alfabeto:
		return "ERRO - A transição " + transicao[0] + " não está no alfabeto - Linha " + str(cont+1) + ": " + linha

	elif transicao[1] != '&' and transicao[1] != '?' and transicao[1] not in aut.alfabetoPilha:
		return "ERRO - A transição " + transicao[1] + " não está no alfabeto de pilha - Linha " + str(cont+1) + ": " + linha

	elif transicao[2] != '&' and transicao[2] != '?' and transicao[2] not in aut.alfabetoPilha:
		return "ERRO - A transição " + transicao[2] + " não está no alfabeto de pilha - Linha " + str(cont+1) + ": " + linha

	transicao = (transicao[0], transicao[1], transicao[2])

	if transicao not in aut.transicoes[estado1].keys():

		aut.transicoes[estado1][transicao] = []

	if estado2 in aut.transicoes[estado1][transicao]:

		arq.close()
		return "ERRO - Transição repetida! - Linha " + str(cont+1) + ": " + linha

	aut.transicoes[estado1][transicao].append(estado2)

	# Caso o autômato seja AFD mas tenha alguma transição que leva a um conjunto de estados
	if aut.tipo == 2 and len(aut.transicoes[estado1][transicao]) != 1:

		arq.close()
		return ("ERRO - O autômato é APD mas tem transição não determinista! - "+estado1+"-"+transicao+"-"
			+str(aut.transicoes[estado1][transicao]))

	return None

# Cria o autômato a partir do arquivo de entrada 
def criaAutomato (aut, arqEntrada):

	if arqEntrada == '':

		return "ERRO - Arquivo inexistente!"

	try:

		arq = open(arqEntrada, "r")

	except:

		return "ERRO - Arquivo inválido!"

	cont = 0 # Coordena o processamento do cabeçalho e do corpo do arquivo
	estadosIF = ['+', '*'] # Símbolos que definem estado inicial e final, respectivamente

	for linha in arq: # Para cada linha do arquivo

		# Caso a linha comece com '#', significa que é a descrição do autômato ou um comentário
		if linha[0] == '#':

			# Apenas o primeiro comentário é tratado como a descrição do autômato
			if aut.descricao == "Autômato sem descrição":
		
				linha = linha.replace('\n', '')
				aut.descricao = linha.replace('#', '')
				aut.grafo.comment = aut.descricao

		# Do contrário, processa normalmente
		else:

			# Cont > 0 significa processamento das transições
			if cont > 0:

				r = None

				if aut.tipo < 3:
					r = constroiAutomatoFinito(linha, aut, cont)

				else:
					r = constroiAutomatoPilha(linha, aut, cont)

				if r != None:
					return r

			# Cont = 0 significa processamento do cabeçalho
			else:

				linha = linha.replace('\n',"")
				valores = linha.split(' ');
				
				aut.tipo = pegaTipo(valores[0]) # Pega o tipo do autômato 

				if aut.tipo == -1:

					arq.close()
					return 'ERRO - Tipo inválido! - ' + valores[0]

				# Tenta armazenar o alfabeto do autômato
				try:
					valores[1] = valores[1].replace('[',"")
					valores[1] = valores[1].replace(']',"")
					valores[1] = valores[1].split(',')
					aut.alfabeto = valores[1]

				except:
					arq.close()
					return 'ERRO - Alfabeto vazio!'

				# Caso seja um AP, tenta armazenar o alfabeto de pilha
				if aut.tipo > 2:

					try:
						valores = valores[2].replace('[',"")
						valores = valores.replace(']',"")
						valores = valores.split(',')
						aut.alfabetoPilha = valores

					except:
						arq.close()
						return 'ERRO - Alfabeto de pilha vazio!'

				if aut.alfabeto[0] == "":

					arq.close()
					return 'ERRO - Alfabeto vazio!'

				else:
					try:
						if aut.alfabetoPilha[0] == "":
		
							arq.close()
							return 'ERRO - Alfabeto de pilha vazio!'
					
					except:
						pass

				cont += 1

	# Formata o nome do estado inicial
	aut.estadoInicial = (aut.estadoInicial.replace("+", "")).replace("*", "")

	# Caso não haja nenhum erro, retorna None
	arq.close()
	return None
