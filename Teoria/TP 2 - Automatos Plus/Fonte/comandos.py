from sys import exit
from os import system, name

def decodificaComando (comando, automato):
	
	estados = []

	if comando == 'q': # Sai do programa
		
		print("<< Saindo...")
		exit()
		return None

	elif comando == 'h': # Exibe a ajuda
		
		print ("<< HELP - Comandos:")
		print ("   :le - Lista os estados do autômato")
		print ("   :li - Mostra o estado inicial do autômato")
		print ("   :lf - Lista os estados finais do autômato")
		print ("   :lt - Lista as transições do autômato")
		print ("   :la - Lista o alfabeto do autômato")
		print ("   :lp - Lista o alfabeto de pilha do autômato")
		print ("   :a - Mostra o tipo do autômato")
		print ("   :d - Mostra a descrição do autômato")
		print ("   :ta - Trocar autômato")
		print ("   :c - Limpa a tela do programa")
		print ("   :h - Exibe a ajuda")
		print ("   :p <palavra> - Mostra o processamento de <palavra> passo a passo")
		print ("   :q - Encerra o programa")
		
		return None

	elif comando == 'c': # Limpa a tela
		
		if name == "posix":

			system("clear")

		else:

			system("cls")
	
		print ("Digite a palavra a ser testada: ")
		
		return None

	elif comando == 'a': # Imprime o tipo do autômato
		
		if automato.tipo == 1:

			print ("<< AFD")

		elif automato.tipo == 2:

			print ("<< AFN")

		elif automato.tipo == 3:

			print ("<< APD")

		else:

			print ("<< APN")

		return None

	elif comando == 'd': # Imprime a descrição do autômato

		if automato.tipo == None:

			print ("<< Autômato sem descrição")

		else:

			if automato.tipo == 1:

				print ("<< AFD: " + automato.descricao)

			elif automato.tipo == 2:

				print ("<< AFN: " + automato.descricao)

			elif automato.tipo == 3:

				print ("<< APD: " + automato.descricao)

			else:
				
				print ("<< APN: " + automato.descricao)

		return None

	elif comando == 'le': # Lista os estados do autõmato

		print ("<< Estados:")

		for estado in automato.transicoes.keys():

			estados.append((estado.replace('*', "")).replace('+', ""))

		print ("   " + str(estados))

		return None

	elif comando == 'li': # Exibe o estado inicial do autõmato

		print ("<< Estado inicial: " + str((automato.estadoInicial.replace('*', "")).replace('+', "")))

		return None

	elif comando == 'lf': # Lista os estados finais do autõmato

		for estado in automato.estadosFinais:

			estados.append((estado.replace('*', "")).replace('+', ""))

		print ("<< Estados finais:\n   " + str(estados))

		return None
	
	elif comando == 'lt': # Exibe a tabela de transições do autômato

		print ("<< Tabela de transições:")


		for estado in automato.transicoes.keys():

			transicoes = []

			for transicao in automato.transicoes[estado]:

				estados = []

				for estadoLinha in automato.transicoes[estado][transicao]:

					estados.append((estadoLinha.replace('*', "")).replace('+', ""))
			
				transicoes.append([transicao, estados])

			print ("   " + str((estado.replace('*', "")).replace('+', "")) + ": " + str(transicoes))

		return None

	elif comando == 'la': # Exibe o alfabeto aceito pelo autõmato

		print ("<< Alfabeto: " + str(automato.alfabeto))
	
		return None

	elif comando == 'lp': # Exibe o alfabeto de pilha do autõmato

		if automato.tipo > 2:
			print ("<< Alfabeto de Pìlha: " + str(automato.alfabetoPilha))

		else:
			print ("<< O autômato não é um Autômato de Pilha")
	
		return None

	elif comando[0] == 'p': # Recebe uma palavra como argumento e exibe o passo-a-passo

		comando = comando.split(' ')
		
		if len(comando) != 2:

			print ("O comando :p espera uma palavra como argumento! - Digite ':h' para ajuda")
			
			return None

		print ("<< Exibindo o passo-a-passo:")
		print(automato.testaPalavra(comando[1], True))
		
		automato.imprimePassoAPasso(comando[1])
		
		return None

	elif len(comando) > 1 and (comando[0], comando[1]) == ('t', 'a'): # Troca o autômato carregado

		comando = comando.split(' ')

		if len(comando) == 2:

			return comando[1] 

		print ("<< Digite o endereço do arquivo de entrada: ")
		arqEntrada = input("\n>> ")
	
		return arqEntrada

	else: # Exibe o uso dos comandos

		print ("Comando inexistente! - Digite ':h' para ajuda")
		
		return None