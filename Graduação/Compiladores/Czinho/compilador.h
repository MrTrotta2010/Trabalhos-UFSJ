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

typedef struct {
    char valor[256];
    int tipo; //Inteiro = 0, float = 1, double = 2, char = 3
    int declarada, inicializada, escopo, linha, coluna, func;
} Simbolo;

typedef struct {
    int tamanho;
    Simbolo *simbolos;
} TabelaSimbolos;

typedef struct elemento *ListaTokens;

//Lista de Tokens
ListaTokens *criaLista();
void liberaLista(ListaTokens *tkl);
int insereToken(ListaTokens *tkl, Token tk);
int printListaToken(ListaTokens *tkl);

//Tabela de símbolos

//Entrada e saída
char *carregaPrograma(char *arquivo);

//Analisador Léxico
int analiseLexica(char *codigo, ListaTokens *listaTokens, ListaTokens *listaErros);
int insereToken(ListaTokens *tkl, Token tk);
Token criaToken (char classe[256], char valor[256], int id, int linha, int coluna);

//Analisador sintático
int analiseSintatica(ListaTokens *listaTokens, ListaTokens *listaErros, TabelaSimbolos *tabelaSimbolos);
int constroiTabelaSimbolos(ListaTokens *listaTokens, TabelaSimbolos *tabelaSimbolos);
void printTabelaSimbolos(TabelaSimbolos tabela);