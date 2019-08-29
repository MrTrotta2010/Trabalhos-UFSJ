#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include <regex.h>

#define NUM_TOKENS 7

typedef struct {
	int id;
	char tipo;
	char valor;
	int linha;
	int coluna;
} Token;

typedef Token *ListaTokens;

//Entrada e saída
char *carregaPrograma(char *arquivo);

//Analisador Léxico
char **carregaTokens();
ListaTokens analiseLexica(char *codigo);