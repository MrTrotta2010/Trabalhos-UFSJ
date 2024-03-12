#include "compilador.h"

struct elemento{
	Token tk;
	struct elemento *prox;
};

typedef struct elemento Elemento;

int estaNaTabela(char *valor, TabelaSimbolos tabela) {

	for (int i = 0; i < tabela.tamanho; i++) {
		if (strcmp(tabela.simbolos[i].valor, valor) == 0) return 1;
	}
	return 0;
}

void criaSimbolo(Simbolo *simbolo, char *valor) {
	strcpy(simbolo->valor, valor);
	simbolo->tipo = -1;
	simbolo->declarada = 0;
	simbolo->inicializada = 0;
	simbolo->escopo = -1;
	simbolo->linha = -1;
	simbolo->coluna = -1;
	simbolo->func = -1;
}

int constroiTabelaSimbolos(ListaTokens *listaTokens, TabelaSimbolos *tabelaSimbolos) {

	Elemento *aux;

	// Percorre a lista de tokens para contar a quantidade de identificadores
	if(*listaTokens == NULL) {
		return 1;
	}

	for (aux = *listaTokens; aux != NULL; aux = aux->prox){
		if (aux->tk.id == 1) {
			if (tabelaSimbolos->simbolos == NULL) {
				tabelaSimbolos->simbolos = malloc(sizeof(Simbolo));
				criaSimbolo(&tabelaSimbolos->simbolos[0], aux->tk.valor);
				tabelaSimbolos->tamanho++;
			} else {
				if (!estaNaTabela(aux->tk.valor, *tabelaSimbolos)) {
					tabelaSimbolos->tamanho++;
					tabelaSimbolos->simbolos = realloc(tabelaSimbolos->simbolos, 
												tabelaSimbolos->tamanho*sizeof(Simbolo));
					criaSimbolo(&tabelaSimbolos->simbolos[tabelaSimbolos->tamanho-1], aux->tk.valor);
				}
			}
		}
	}

	return 0;
}

void printTabelaSimbolos(TabelaSimbolos tabela) {
	for (int i = 0; i < tabela.tamanho; i++) {
		if (tabela.simbolos[i].func == 0) {
			printf("Variável %s do tipo %d ", tabela.simbolos[i].valor, tabela.simbolos[i].tipo);
		} else {
			printf("Função %s do tipo %d ", tabela.simbolos[i].valor, tabela.simbolos[i].tipo);
		}
		if (tabela.simbolos[i].declarada == 1) {
			printf("foi declarada na linha %d, coluna %d ", tabela.simbolos[i].linha, tabela.simbolos[i].coluna);
		} else {
			printf("não foi declarada ");
		}
		if (tabela.simbolos[i].inicializada == 1) {
			printf("e foi inicializada\n");
		} else {
			printf("e não foi inicializada\n");
		}
	}
}

int isTipo(char *valor, int *tipo) {
	
	if (strcmp(valor, "int") == 0) {
		if (tipo != NULL) *tipo = 0;
		return 1;
	}		
	else if (strcmp(valor, "float") == 0) {
		if (tipo != NULL) *tipo = 1;
		return 1;
	}		
	else if (strcmp(valor, "double") == 0) {
		if (tipo != NULL) *tipo = 2;
		return 1;
	}	
	else if (strcmp(valor, "char") == 0) {
		if (tipo != NULL) *tipo = 3;
		return 1;
	}
	return 0;
}

void declaraSimbolo(char *simbolo, int tipo, int linha, int coluna, int func, TabelaSimbolos *tabela) {
	for (int i = 0; i < tabela->tamanho; i++) {
		if (strcmp(tabela->simbolos[i].valor, simbolo) == 0) {
			tabela->simbolos[i].declarada = 1;
			tabela->simbolos[i].tipo = tipo;
			tabela->simbolos[i].linha = linha;
			tabela->simbolos[i].coluna = coluna;
			tabela->simbolos[i].func = func;
			break;
		}
	}
}

void inicializaSimbolo(char *simbolo, TabelaSimbolos *tabela) {
	for (int i = 0; i < tabela->tamanho; i++) {
		if (strcmp(tabela->simbolos[i].valor, simbolo) == 0) {
			tabela->simbolos[i].inicializada = 1;
			break;
		}
	}
}

int reconheceBloco(Elemento **aux, ListaTokens *listaErros, TabelaSimbolos *tabelaSimbolos);

int reconhecePrimArg(Elemento **aux, ListaTokens *listaErros) {
	// Tipo
	if (isTipo((*aux)->tk.valor, NULL)) {
		*aux = (*aux)->prox;
		// Identificador
		if ((*aux)->tk.id == 1) {
			return 1;
		} else {
			Token errToken = criaToken("ERRO - esperava-se um identificador e recebeu-se", (*aux)->tk.valor, -1, (*aux)->tk.linha, (*aux)->tk.linha);
			insereToken(listaErros, errToken);
		}
	}
	return 0;
}

int reconheceListaArgs(Elemento **aux, ListaTokens *listaErros) {
	//Vírgula
	if (strcmp((*aux)->tk.valor, ",") == 0) {
		// Tipo
		*aux = (*aux)->prox;
		if (isTipo((*aux)->tk.valor, NULL)) {
			*aux = (*aux)->prox;
			// Identificador
			if ((*aux)->tk.id == 1) {
				*aux = (*aux)->prox;
				// Fecha parênteses
				if (strcmp((*aux)->tk.valor, ")") == 0) return 1;
				// Outro argumentos
				else if (reconheceListaArgs(aux, listaErros)) return 1;
				else {
					Token errToken = criaToken("ERRO - esperava-se um \")\" e recebeu-se", (*aux)->tk.valor, -1, (*aux)->tk.linha, (*aux)->tk.linha);
					insereToken(listaErros, errToken);	
				}
			} else {
				Token errToken = criaToken("ERRO - esperava-se um identificador e recebeu-se", (*aux)->tk.valor, -1, (*aux)->tk.linha, (*aux)->tk.linha);
				insereToken(listaErros, errToken);
			}
		} else {
			Token errToken = criaToken("ERRO - esperava-se um tipo e recebeu-se", (*aux)->tk.valor, -1, (*aux)->tk.linha, (*aux)->tk.linha);
			insereToken(listaErros, errToken);
		}
	} else {
		Token errToken = criaToken("ERRO - esperava-se \",\" e recebeu-se", (*aux)->tk.valor, -1, (*aux)->tk.linha, (*aux)->tk.linha);
		insereToken(listaErros, errToken);
	}
	return 0;
}

int reconheceFuncao(Elemento **aux, ListaTokens *listaErros, TabelaSimbolos *tabelaSimbolos) {
	// Tem argumentos
	if (reconhecePrimArg(aux, listaErros)) {
		*aux = (*aux)->prox;
		if (reconheceListaArgs(aux, listaErros)) {
			*aux = (*aux)->prox;
			// Verifica se é só o cabeçalho
			if (strcmp((*aux)->tk.valor, ";") == 0) {
				printf("Cabeçalho de função\n");
                return 1;
			}
			else if (strcmp((*aux)->tk.valor, "{") == 0) {
				printf("Declaração de função\n");
				*aux = (*aux)->prox;
				if (reconheceBloco(aux, listaErros, tabelaSimbolos)) return 1;
			}
		}
	}
	// Nenhum argumento
	else if (strcmp((*aux)->tk.valor, ")") == 0) {
		*aux = (*aux)->prox;
		// Verifica se é só o cabeçalho
		if (strcmp((*aux)->tk.valor, ";") == 0) {
			printf("Cabeçalho de função\n");
            return 1;
		}
		// Verifica se é declaração
		else if (strcmp((*aux)->tk.valor, "{") == 0) {
			printf("Declaração de função\n");
			*aux = (*aux)->prox;
			if (reconheceBloco(aux, listaErros, tabelaSimbolos)) return 1;
		}
	}
	else {
		//Erro
		Token errToken = criaToken("ERRO - símbolo inesperado", (*aux)->tk.valor, -1, (*aux)->tk.linha, (*aux)->tk.linha);
		insereToken(listaErros, errToken);
	}

    return 0;
}

int reconheceDecProx(Elemento **aux, ListaTokens *listaErros, TabelaSimbolos *tabelaSimbolos, int tipo) {
	Elemento *prox = (*aux)->prox;
    int r = 0;

	if (strcmp(prox->tk.valor, ";") == 0) {
		printf("Declaração de variável\n");
		declaraSimbolo((*aux)->tk.valor, tipo, (*aux)->tk.linha, (*aux)->tk.coluna, 0, tabelaSimbolos);
        r = 1;
	} 
	else if (strcmp(prox->tk.valor, "(") == 0) {
		prox = prox->prox;
		if (reconheceFuncao(&prox, listaErros, tabelaSimbolos)) r = 1;
	} else {
		Token errToken = criaToken("ERRO - Esperava-se um identificador e recebeu-se", (*aux)->tk.valor, -1, (*aux)->tk.linha, (*aux)->tk.linha);
		insereToken(listaErros, errToken);
	}
	*aux = prox;
    return r;
}

int reconheceDeclaracao(Elemento **aux, ListaTokens *listaErros, TabelaSimbolos *tabelaSimbolos, int tipo) {
	//Identificador
	if ((*aux)->tk.id == 1) {
		if (reconheceDecProx(aux, listaErros, tabelaSimbolos, tipo)) return 1;
	} else {
		Token errToken = criaToken("ERRO - Esperava-se um identificador recebeu-se", (*aux)->tk.valor, -1, (*aux)->tk.linha, (*aux)->tk.linha);
		insereToken(listaErros, errToken);
	}
    return 0; 
}

int isComparacao(char *valor) {
	if (strcmp(valor, "==") == 0) return 1;
	else if (strcmp(valor, "<") == 0) return 1;
	else if (strcmp(valor, ">") == 0) return 1;
	else if (strcmp(valor, "<=") == 0) return 1;
	else if (strcmp(valor, ">=") == 0) return 1;
	else if (strcmp(valor, "!=") == 0) return 1;
	return 0;
}

int aritmetica(char *valor) {
	if (strcmp(valor, "+") == 0) return 1;
	else if (strcmp(valor, "-") == 0) return 1;
	else if (strcmp(valor, "*") == 0) return 1;
	else if (strcmp(valor, "/") == 0) return 1;
	return 0;
}

int aritmeticaDupla(char *valor) {
	if (strcmp(valor, "++") == 0) return 1;
	else if (strcmp(valor, "--") == 0) return 1;
	return 0;
}

int aritmeticaDuplaComposto(char *valor) {
	if (strcmp(valor, "+=") == 0) return 1;
	else if (strcmp(valor, "-=") == 0) return 1;
	else if (strcmp(valor, "*=") == 0) return 1;
	else if (strcmp(valor, "/=") == 0) return 1;
	return 0;
}

int opBinario(char *valor) {
	return (aritmetica(valor) || aritmeticaDuplaComposto(valor));
}

int reconheceArgumentosChamadaDeFuncao(Elemento **aux, ListaTokens *listaErros) {
	//Nenhum argumento
	if (strcmp((*aux)->prox->tk.valor, ")") == 0) return 1;
	// Identificador
    else if ((*aux)->tk.id == 1) {
        *aux = (*aux)->prox;
        if (strcmp((*aux)->tk.valor, ",") == 0) {
            *aux = (*aux)->prox;
            if (reconheceArgumentosChamadaDeFuncao(aux, listaErros)) return 1;
        }
        else if (strcmp((*aux)->prox->tk.valor, ")") == 0) return 1;
    }
	return 0; 
}

int reconheceChamadaDeFuncao(Elemento **aux, ListaTokens *listaErros) {
	
	//Abre parenteses
	if (strcmp((*aux)->tk.valor, "(") == 0) {
	    *aux = (*aux)->prox;
		//Argumentos
		if (reconheceArgumentosChamadaDeFuncao(aux, listaErros)) {
			*aux = (*aux)->prox;
			// Feccha parenteses
			if (strcmp((*aux)->tk.valor, ")") == 0) {
                printf("Chamada de função\n");
                return 1;
            }
		}
	}

	return 0;
}

int valorOp(int id) {
	return (id == 1 || id == 2);
}

int reconheceOpAritmetica(Elemento **aux, ListaTokens *listaErros) {
    Elemento *temp = *aux;
    int r = 0;

    if (aritmetica((*aux)->tk.valor)) {
        *aux = (*aux)->prox;
        if (valorOp((*aux)->tk.id)) r = 1;
        else *aux = temp;
    }
    else if (aritmeticaDupla((*aux)->tk.valor)) r = 1;
    else *aux = temp;
	return r;
}

int reconheceOpLogica(Elemento **aux, ListaTokens *listaErros) {
    Elemento *temp = *aux;
    int r = 0;

    if ((*aux)->tk.id == 5) {
        *aux = (*aux)->prox;
        if (valorOp((*aux)->tk.id)) r = 1;
        else *aux = temp; 
    }
    else *aux = temp;
	return r;
}

int reconheceOperacao(Elemento **aux, ListaTokens *listaErros) {
    Elemento *temp = *aux;
    int r = 0;
	if (reconheceOpAritmetica(aux, listaErros)) r = 1;
	else if (reconheceOpLogica(aux, listaErros)) r = 1;
    if (r == 0)	*aux = temp;
    else printf("Expressão\n");
    return r;
}

int reconheceAtribuicao(Elemento **aux, ListaTokens *listaErros) {
	//Identificador
	if ((*aux)->tk.id == 1) {
		if (strcmp((*aux)->prox->tk.valor, ";") == 0) {
			return 1;
		} else {
            *aux = (*aux)->prox;
            //Operação
            if (reconheceOperacao(aux, listaErros)) return 1;
            //Função
            else if (reconheceChamadaDeFuncao(aux, listaErros)) return 1;
            else {
                Token errToken = criaToken("ERRO - esperava-se um valor e recebeu-se", (*aux)->tk.valor, -1, (*aux)->tk.linha, (*aux)->tk.linha);
                insereToken(listaErros, errToken);
            }
        }
	}
    //Numero
	else if ((*aux)->tk.id == 2) {
		if (strcmp((*aux)->prox->tk.valor, ";") == 0) {
			return 1;
		} else {
            *aux = (*aux)->prox;
            //Operação
            if (reconheceOperacao(aux, listaErros)) return 1;
            else {
                Token errToken = criaToken("ERRO - esperava-se um valor e recebeu-se", (*aux)->tk.valor, -1, (*aux)->tk.linha, (*aux)->tk.linha);
                insereToken(listaErros, errToken);
            }
        }
	}
	else {
		Token errToken = criaToken("ERRO - esperava-se uma valor e recebeu-se", (*aux)->tk.valor, -1, (*aux)->tk.linha, (*aux)->tk.linha);
		insereToken(listaErros, errToken);
	}
	return 0;
}

int reconheceExpressao(Elemento **aux, ListaTokens *listaErros, TabelaSimbolos *tabelaSimbolos) {

	// Atribuição
	*aux = (*aux)->prox;
    if (strcmp((*aux)->tk.valor, ";") == 0) {
        printf("Valorn\n");
        return 1;
    }
	else if (strcmp((*aux)->tk.valor, "=") == 0) {
		*aux = (*aux)->prox;
		if (reconheceAtribuicao(aux, listaErros)) {
			*aux = (*aux)->prox;
			if (strcmp((*aux)->tk.valor, ";") == 0) return 1;
			else {
				Token errToken = criaToken("ERRO - esperava-se um \";\" e recebeu-se", (*aux)->tk.valor, -1, (*aux)->tk.linha, (*aux)->tk.linha);
				insereToken(listaErros, errToken);
			}
		}
	}
	else if (reconheceOperacao(aux, listaErros)) {
		*aux = (*aux)->prox;
		if (strcmp((*aux)->tk.valor, ";") == 0) return 1;
		else {
			Token errToken = criaToken("ERRO - esperava-se um \";\" e recebeu-se", (*aux)->tk.valor, -1, (*aux)->tk.linha, (*aux)->tk.linha);
			insereToken(listaErros, errToken);
		}
	}
	else {
		Token errToken = criaToken("ERRO - esperava-se uma expressão e recebeu-se", (*aux)->tk.valor, -1, (*aux)->tk.linha, (*aux)->tk.linha);
		insereToken(listaErros, errToken);
	}
	
	return 0;
}

int reconheceInclude(Elemento **aux) {
	if (strcmp((*aux)->tk.valor, "<") == 0) {
		*aux = (*aux)->prox;
		if ((*aux)->tk.id == 9) {
			*aux = (*aux)->prox;
			if (strcmp((*aux)->tk.valor, ">") == 0) {
				printf("Include\n");
                return 1;
			}
		}
	}
	else if (strcmp((*aux)->tk.valor, "\"") == 0) {
		*aux = (*aux)->prox;
		if ((*aux)->tk.id == 3) {
			*aux = (*aux)->prox;
			if (strcmp((*aux)->tk.valor, "\"") == 0) {
				printf("Include\n");
                return 1;
			}
		}
	}
    return 0;
}

int reconheceDiretiva(Elemento **aux) {

	if (strcmp((*aux)->tk.valor, "include") == 0) {
		*aux = (*aux)->prox;
		if (reconheceInclude(aux)) return 1;
	}
    return 0;
}

int reconheceReturn(Elemento **aux, ListaTokens *listaErros, TabelaSimbolos *tabelaSimbolos) {
    *aux = (*aux)->prox;
    if ((*aux)->tk.id == 1 || (*aux)->tk.id == 2) {
        if (reconheceExpressao(aux, listaErros, tabelaSimbolos)) {
            printf("Return\n");
            return 1;
        }
    }
    return 0;
}

int reconheceStatement(Elemento **aux, ListaTokens *listaErros, TabelaSimbolos *tabelaSimbolos, int *tipo) {

	if ((*aux)->tk.id == 0) {
		
		// Declaração
		if (isTipo((*aux)->tk.valor, tipo)) {
			*aux = (*aux)->prox;
			reconheceDeclaracao(aux, listaErros, tabelaSimbolos, *tipo);
		}
        //Return
        else if (strcmp((*aux)->tk.valor, "return") == 0) {
            if (reconheceReturn(aux, listaErros, tabelaSimbolos)) return 1;
        }
	}

	// Expressão começa com identificador
	else if (valorOp((*aux)->tk.id)) {
		if (reconheceExpressao(aux, listaErros, tabelaSimbolos)) return 1;
	}

	//Diretiva
	else if ((*aux)->tk.id == 8) {
		if (reconheceDiretiva(aux)) return 1;
	}

    return 0;
}

int reconheceBloco(Elemento **aux, ListaTokens *listaErros, TabelaSimbolos *tabelaSimbolos) {
	
	int tipo = 0;

    if (reconheceStatement(aux, listaErros, tabelaSimbolos, &tipo)) {
        *aux = (*aux)->prox;
        if (strcmp((*aux)->tk.valor, "}") == 0) {
            return 1;
        }
        else if (reconheceBloco(aux, listaErros, tabelaSimbolos)) return 1;
    }

    return 0;
}

int analiseSintatica(ListaTokens *listaTokens, ListaTokens *listaErros, TabelaSimbolos *tabelaSimbolos) {

	// Percorre a lista de tokens para contar a quantidade de identificadores
	if(*listaTokens == NULL) {
		return -1;
	}
	Elemento *aux = *listaTokens;
	int tipo;

	while (aux != NULL) {
		//printf("%s\n", aux->tk.valor);

		reconheceBloco(&aux, listaErros, tabelaSimbolos);

		aux = aux->prox;
	}

	return 0;
}