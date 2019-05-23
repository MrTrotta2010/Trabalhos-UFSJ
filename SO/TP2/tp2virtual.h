#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "colors.h"

#define KB 1024
#define TRUE 1
#define FALSE 0

unsigned pagLidas;
unsigned pagEscritas;
unsigned pageHit;
unsigned pageFault;
unsigned debug;
unsigned escritasDisco;

typedef struct {

	int substituicao;
	char nomeSubstituicao[256];
	unsigned tamPag;
	unsigned tamMem;
	char arqEntrada[256];
	unsigned debug;

} Configuracao;

typedef struct Pagina {

	_Bool mudou;
	_Bool valido;
	_Bool referenciado;
	unsigned indiceFila;
	unsigned paginaVirtual;
	unsigned moldura;
	unsigned indiceTabela;
	struct Pagina *prox;

} Pagina;

typedef struct {

	Pagina *pagina;
	unsigned numMolduras;
	unsigned moldurasUsadas;
	_Bool *statusMemoria;
	unsigned *referenciado;

} TabelaPagina;

typedef struct {

	Pagina *paginas;
	unsigned final;

} Fila;

Configuracao* recebeConfig(int numArg, char **argv);

_Bool configValida(Configuracao *config);

void imprimeLog(Configuracao *config, unsigned pagLidas, unsigned pagEscritas);

TabelaPagina inicializaTabela(Configuracao *config);

void inicializaPagina(Pagina *pagina);

Fila *criaFila (unsigned tamanho);

void insereFila (Fila *fila, Pagina *pagina, _Bool referenciar);

void reorganizaFila (Fila *fila, unsigned posicao, _Bool referenciar);

unsigned removeFila (Fila *fila, unsigned posicao);

void copyPagina(Pagina *pagDestino, Pagina *pagFonte);

void imprimeFila(Fila *fila);
