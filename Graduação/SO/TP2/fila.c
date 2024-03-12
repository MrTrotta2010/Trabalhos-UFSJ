#include "tp2virtual.h"

//Fila criada na implementação do Segunda_chance

//cria fila
Fila *criaFila (unsigned tamanho) {

	Fila *fila = (Fila*)malloc(sizeof(Fila));
	fila->paginas = (Pagina*)malloc(tamanho*sizeof(Pagina));
	
	for(unsigned i = 0; i < tamanho; i++) inicializaPagina(&(fila->paginas[i]));

	fila->final = 0;

	return fila;

}

//insere uma pagina na fila
void insereFila (Fila *fila, Pagina *pagina, _Bool referenciar) {

	fila->paginas[fila->final].indiceTabela = pagina->indiceTabela; 
	fila->paginas[fila->final].paginaVirtual = pagina->paginaVirtual; 
	fila->paginas[fila->final].moldura = pagina->moldura; 
	fila->paginas[fila->final].indiceFila = fila->final; 
	fila->paginas[fila->final].referenciado = referenciar; 

	fila->final++;
}

//reorganiza a fila quando uma pagina é referenciada
void reorganizaFila (Fila *fila, unsigned posicao, _Bool referenciar) {

	Pagina *aux = (Pagina*)malloc(sizeof(Pagina));

	aux->indiceTabela = fila->paginas[posicao].indiceTabela; 
	aux->paginaVirtual = fila->paginas[posicao].paginaVirtual; 
	aux->moldura = fila->paginas[posicao].moldura; 
	aux->referenciado = referenciar; 
	aux->indiceFila = -1;

	for (unsigned i = posicao; i < fila->final-1; i++) {
	
		fila->paginas[i] = fila->paginas[i+1];
		fila->paginas[i].indiceFila--;

	}

	fila->final--;

	insereFila(fila, aux, referenciar);

}

//remove uma página da fila quando ela removida da tabela de páginas
unsigned removeFila (Fila *fila, unsigned posicao) {

	unsigned moldura = fila->paginas[posicao].moldura;

	for (unsigned i = posicao; i < fila->final-1; i++){
	
		fila->paginas[i] = fila->paginas[i+1];
		fila->paginas[i].indiceFila--;

	}

	fila->final--;

	return moldura;

}