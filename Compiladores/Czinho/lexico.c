#include "compilador.h"

int separador (char caractere) {

	char separadores[] = {' ', '.', ',', ';', ':','(', ')', '{', '}', '[', ']', '=', '#'};
	for (int i = 0; i < strlen(separadores); i++) {
		if (separadores[i] == caractere) return 1;
	}
	return 0;
}

int opAritmetico (char caractere) {

	char operadoresArit[] = {'+', '-', '*', '/', '%'};
	for (int i = 0; i < strlen(operadoresArit); i++) {
		if (operadoresArit[i] == caractere) return 1;
	}
	return 0;
}

int opLogico (char caractere) {

	char operadoresLog[] = {'&', '|', '!', '?', '<', '>'};
	for (int i = 0; i < strlen(operadoresLog); i++) {
		if (operadoresLog[i] == caractere) {
			return 1;
		}
	}
	return 0;
}

int reservada (char palavra[256]) {

	char reservadas[32][10] = {"auto", "break", "case", "const", "continue", "default", "do", "double", "else", "enum", "extern", "float", "for", "goto", "if", "int", "long", "register", "return", "short", "signed", "sizeof", "static", "struct", "switch", "typedef", "union", "unsigned", "void", "volatile", "while"};
	for (int i = 0; i < 32; i++) {
		if (strcmp(reservadas[i], palavra) == 0) return 1;
	}
	return 0;
}

Token criaToken (char classe[256], char valor[256], int id, int linha, int coluna) {

	Token tk;

	strcpy(tk.classe, classe);
	strcpy(tk.valor, valor);
	tk.id = id;
	tk.linha = linha;
	tk.coluna = coluna;

	return tk;
}

int analiseLexica (char *codigo, ListaTokens *listaTokens, ListaTokens *listaErros) {

    long unsigned int pivo = 0, tamanho = strlen(codigo); 
	int sentinela, posicaoPal, linha = 1, coluna = 1, deuErro = FALSE;
	char caractere;

	//Le o código caractere por caractere
	while (pivo < tamanho) {
        
		caractere = codigo[pivo];
		sentinela = pivo;
		posicaoPal = 0;
		char palavra[256] = "\0";


		//Contador de linha
		if (caractere == '\n') {
			linha++;
			coluna = 1;
		}

		//Diretivas de compilação
		if (caractere == '#') {
			sentinela++;
			coluna++;
			caractere = codigo[sentinela];
			while (isalpha(caractere)) {
				palavra[posicaoPal] = caractere;
				posicaoPal++;
				sentinela++;
				coluna++;
				caractere = codigo[sentinela];
			}
			//Erros:
			// if (caractere == '\n') {
			// 	linha++;
			// 	coluna = 1;
			// }
			Token novoToken = criaToken("DIRETIVA", palavra, 8, linha, coluna-1);
			insereToken(listaTokens, novoToken);
			pivo = sentinela;
		}

		//Identificadores e outras palavras reservadas
		else if (isalpha(caractere) || caractere == '_' || caractere == '@') {
			int erro = FALSE;
            char aux = codigo[pivo-1];
			if (caractere == '@' || caractere == '#' || isdigit(caractere)) {
				erro = TRUE;
			}
            if (aux != '<') {
                while (!separador(caractere) && !opAritmetico(caractere) && !opLogico(caractere) && caractere != '\n') {
                    palavra[posicaoPal] = caractere;
                    posicaoPal++;
                    sentinela++;
                    coluna++;
                    caractere = codigo[sentinela];
                }
                //Erros:
                for (int i = 0; i < strlen(palavra); i++) {
                    if (palavra[i] == '@' || palavra[i] == '#') {
                        erro = TRUE;
                        break;
                    }
                }
                if (erro) {
                    deuErro = TRUE;
                    Token errToken = criaToken("ERRO!", palavra, -1, linha, coluna-1);
                    insereToken(listaErros, errToken);
                } else {
                    Token novoToken;
                    if (reservada(palavra))
                        novoToken = criaToken("RESERVADA", palavra, 0, linha, coluna-1);
                    else {
                        novoToken = criaToken("IDENTIFICADOR", palavra, 1, linha, coluna-1);
                    }

                    insereToken(listaTokens, novoToken);
                }
            } else {
                while (caractere != '>') {
                    palavra[posicaoPal] = caractere;
                    posicaoPal++;
                    sentinela++;
                    coluna++;
                    caractere = codigo[sentinela];
                }
                Token novoToken = criaToken("BIBLIOTECA", palavra, 9, linha, coluna-1);
                insereToken(listaTokens, novoToken);
            }
			pivo = sentinela;
		}

		//Números
		else if (isdigit(caractere)) {
			while (!separador(caractere) && !opAritmetico(caractere) && !opLogico(caractere) && caractere != '\n') {
				palavra[posicaoPal] = caractere;
				posicaoPal++;
				sentinela++;
				coluna++;
				caractere = codigo[sentinela];
			}
			if (caractere == '\n') {
				linha++;
				coluna = 1;
			}
			for (int i = 0; i < strlen(palavra); i++) {
				if (palavra[i] == '@' || palavra[i] == '#') {
					deuErro = TRUE;
					Token errToken = criaToken("ERRO!", palavra, -1, linha, coluna-1);
					insereToken(listaErros, errToken);
					break;
				}
			}
			Token novoToken = criaToken("NUMERO", palavra, 2, linha, coluna-1);
			insereToken(listaTokens, novoToken);
			pivo = sentinela;
		}

		//Literais (chars são tratados como literais)
		else if (caractere == '"' || caractere == '\'') {
			char caractereAnt = caractere;
			sentinela++;
			coluna++;
			caractere = codigo[sentinela];
			while (caractere != caractereAnt) {
				if (caractere == '\n') {
					linha++;
				}
				palavra[posicaoPal] = caractere;
				posicaoPal++;
				sentinela++;
				coluna++;
				caractere = codigo[sentinela];
			}
			Token novoToken = criaToken("LITERAL", palavra, 3, linha, coluna-1);
			insereToken(listaTokens, novoToken);
			pivo = sentinela+1;
		}

		//Operadores aritméticos, comentários e números negativos
		else if (opAritmetico(caractere)) {
			int op = TRUE;
			int contLinha = 0;
			palavra[0] = caractere;
			char caractereAnt = caractere;
			sentinela++;
			coluna++;
			caractere = codigo[sentinela];
			//Alguns operadores são duplos
			if (caractere == '=' || ((caractereAnt == '+' || caractereAnt == '-') && (caractereAnt == caractere))) {
				palavra[1] = caractere;
				sentinela++;
			}
			//O operador '/' pode indicar um comentário
			else if (caractereAnt == '/') {
				if (caractere == '/') { //Comentários de uma linha
					op = FALSE;
					coluna++;
					sentinela++;
					caractere = codigo[sentinela];
					while (caractere != '\n') {
						palavra[posicaoPal] = caractere;
						posicaoPal++;
						coluna++;
						sentinela++;
						caractere = codigo[sentinela];
					}
				}
				else if (caractere == '*') { /*Comentários de múltiplas linhas*/
					op = FALSE;
					coluna++;
					sentinela++;
					caractere = codigo[sentinela];
					while (caractere != '*') {
						if (caractere == '\n') {
							linha++;
							contLinha++;
						}
						palavra[posicaoPal] = caractere;
						posicaoPal++;
						coluna++;
						sentinela++;
						caractere = codigo[sentinela];
					}
					coluna++;
					sentinela++;
					caractere = codigo[sentinela];
					if (caractere == '/') { //Fechou o comentário
						coluna++;
						sentinela++;
					} else { //Não fechou o comentário

					}
				}
			}
			else if ((caractereAnt == '+' || caractereAnt == '-') && isdigit(caractere)) {
				posicaoPal = 1;
				if (caractereAnt == '+')
					posicaoPal--;
				op ++;
				while (!separador(caractere) && !opAritmetico(caractere) && !opLogico(caractere) && caractere != '\n') {
					palavra[posicaoPal] = caractere;
					posicaoPal++;
					sentinela++;
					coluna++;
					caractere = codigo[sentinela];
				}
				for (int i = 0; i < strlen(palavra); i++) {
					if (palavra[i] == '@' || palavra[i] == '#') {
						deuErro = TRUE;
						Token errToken = criaToken("ERRO!", palavra, -1, linha, coluna-1);
						insereToken(listaErros, errToken);
						break;
					}
				}
			}
			Token novoToken;
			if (op == TRUE)
				novoToken = criaToken("OPERADOR_ARITMETICO", palavra, 4, linha, coluna);
			else if (op == 2)			
				novoToken = criaToken("NUMERO", palavra, 2, linha, coluna);
			else
				novoToken = criaToken("COMENTARIO", palavra, 7, linha-contLinha, coluna);
			insereToken(listaTokens, novoToken);
			pivo = sentinela;
		}

		//Operadores lógicos
		else if (opLogico(caractere)) {
			palavra[0] = caractere;
			char caractereAnt = caractere;
			sentinela++;
			coluna++;
			caractere = codigo[sentinela];
			//Alguns operadores são duplos
			if ((caractereAnt == '&' || caractereAnt == '|') && (caractereAnt == caractere)) {
				palavra[1] = caractere;
				sentinela++;
			}
			else if ((caractereAnt == '<' || caractereAnt == '>' || caractereAnt == '=') && (caractere == '=')) {
				palavra[1] = caractere;
				sentinela++;
			}
            Token novoToken = criaToken("OPERADOR_LOGICO", palavra, 5, linha, coluna);
			insereToken(listaTokens, novoToken);
			pivo = sentinela;
		}

		//Separadores
		else if (separador(caractere) && caractere != ' ') {
			sentinela++;
			coluna++;
			palavra[0] = caractere;
			Token novoToken = criaToken("SEPARADOR", palavra, 6, linha, coluna-1);
			insereToken(listaTokens, novoToken);
			pivo = sentinela;
		}

		else {
			pivo++;
			coluna++;
		}
    }

    return deuErro;
} 