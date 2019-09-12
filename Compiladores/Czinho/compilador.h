#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include <ctype.h>

#define NUM_TOKENS 8
#define TRUE 1
#define FALSE 0

typedef struct {
	char classe[256], valor[256];
	int id, linha, coluna;
} Token;

typedef struct elemento *ListaTokens;

//Lista dinâmica
ListaTokens *criaLista();
void liberaLista(ListaTokens *tkl);
int insereToken(ListaTokens *tkl, Token tk);
int printListaToken(ListaTokens *tkl);

//Entrada e saída
char *carregaPrograma(char *arquivo);

//Analisador Léxico
ListaTokens *analiseLexica(char *codigo);