import sys
from entrada_saida import *
from automato import *
from comandos import *

if __name__ == "__main__":

	# Recebe o arquivo de entrada por argumentos
	arqEntrada = pegaArqEntrada(sys.argv)

	automato = Automato()

	# Tenta criar o automato a partir do arquvo de entrada
	retorno = criaAutomato(automato, arqEntrada)

	if retorno != None:

		if arqEntrada == "": # Se não houver arquivo de entrada, pede-se um

			arqEntrada = decodificaComando('ta', automato) # Pede o arquivo

			if arqEntrada == ":q": # Caso o usuário queira encerrar o programa
				
				decodificaComando('q', automato)

			# Tenta criar o autômato
			retorno = criaAutomato(automato, arqEntrada)

			if retorno != None:

				# Se não conseguir, sai do programa
				print (retorno)
				sys.exit()

		else: # Se não conseguir criar o autômato, sai do programa

			print (retorno)
			sys.exit()

	print ("\nAutômato carregado com sucesso!")
	decodificaComando('d', automato) # Imprime a descrição do autômato

	palavra = ''

	# Indica se o usuário deseja exibir o passo-a-passo
	passoAPasso = False

	print ("\nDigite a palavra a ser testada: ")

	while True: # Repete até o usuário encerrar o programa

		palavra = input("\n>> ")

		if palavra != ":":

			# Caso a palavra seja um comando não vazio
			if palavra != '' and palavra[0] == ':':

				# Caso a decodificação do comando retorne uma string,
				# signifique que o usuário deseja carregar um autômato
				arqEntrada = decodificaComando(palavra[1:len(palavra)], automato)				

				if arqEntrada != '' and arqEntrada != None:
					
					automato.destroiAutomato()

					retorno = criaAutomato(automato, arqEntrada)

					if retorno != None:

						print (retorno)

					else:
						
						print ("\nAutômato carregado com sucesso!")
						decodificaComando('d', automato)
						print ("\nDigite a palavra a ser testada: ")

				elif arqEntrada == '':

					print ("ERRO - Arquivo Inválido!")

			else:

				# Caso o usuário não digite um comando, o autômato testa a
				#palavra
				print("<< "+automato.testaPalavra(palavra, False))

		else:

			# Caso o usuário digite um comando vazio, imprime o uso
			decodificaComando('nada', automato)
