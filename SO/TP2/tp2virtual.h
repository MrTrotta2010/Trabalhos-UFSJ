#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "cores.h"

#define KB 1024
#define TRUE 1
#define FALSE 0

unsigned pagLidas;
unsigned pagEscritas;
unsigned pageHit;
unsigned pageFault;
unsigned debug;

//guarda todas configurações para criação da tabela
typedef struct {

	int substituicao;
	char nomeSubstituicao[256];
	unsigned tamPag;
	unsigned tamMem;
	char arqEntrada[256];
	unsigned debug;

} Configuracao;

//uma página da tabela de páginas
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
	//posiçoes usadas na memória/tabela
	unsigned moldurasUsadas;
	//representa os espaços cheios e vazios na memoria
	_Bool *statusMemoria;
	//representa as páginas referenciadas e não referenciadas da tabela
	unsigned *referenciado;

} TabelaPagina;

//utilizada em Segunda_chance
typedef struct {

	Pagina *paginas;
	unsigned final;

} Fila;

/*ENTRADA E SAÍDA*/

Configuracao* recebeConfig(int numArg, char **argv);

void imprimeLog(Configuracao *config, unsigned pagLidas, unsigned pagEscritas);

void printTabela(TabelaPagina *tabelaPag, char titulo[256], int cor);

void printMemoria(TabelaPagina *tabelaPag, char titulo[256], int cor);

/*TABELA DE PÁGINAS*/

TabelaPagina inicializaTabela(Configuracao *config);

void inicializaPagina(Pagina *pagina);

Pagina * criaPagina();

int posicaoMemoria(TabelaPagina *tabelaPag);
	
int PaginaVirtualQueTaNaMolduraQueVouLimparDaMemoria(Pagina *pagina, int moldura);

void copiaPagina(Pagina *pagDestino, Pagina *pagFonte);

unsigned retiraPagina(TabelaPagina *tabelaPag, Fila *filaPaginas, int substituicao);

void inserePagina(TabelaPagina *tabelaPag, Fila *filaPaginas, unsigned molduraVaga, int substituicao, unsigned clock, unsigned indiceTabela, char rw, unsigned paginaVirtual);

int isPageFault(TabelaPagina *tabelaPagina, Pagina *pagina, Fila *filaPaginas, int substituicao, unsigned paginaVirtual, unsigned clock, char rw);

int memCheia(TabelaPagina *tabelaPagina, long unsigned tamMemoria);

/*FILA DE PÁGINAS NA MEMÓRIA*/

Fila *criaFila (unsigned tamanho);

void insereFila (Fila *fila, Pagina *pagina, _Bool referenciar);

void reorganizaFila (Fila *fila, unsigned posicao, _Bool referenciar);

unsigned removeFila (Fila *fila, unsigned posicao);

void imprimeFila(Fila *fila);

/*ALGORITMOS DE SUBSTITUIÇÃO*/

unsigned lru(TabelaPagina * tabelaPagina);

unsigned nru(TabelaPagina *tabelaPagina);

unsigned segundaChance(TabelaPagina *tabelaPagina, Fila *filaPaginas);

unsigned escolheMoldura(TabelaPagina *tabelaPagina, Fila *filaPaginas, int substituicao);

void resetaReferenciado(TabelaPagina *tabelaPagina);