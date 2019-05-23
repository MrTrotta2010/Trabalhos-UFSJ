#include "tp2virtual.h"

Fila *criaFila (unsigned tamanho) {

	Fila *fila = (Fila*)malloc(sizeof(Fila));
	fila->paginas = (Pagina*)malloc(tamanho*sizeof(Pagina));
	
	for(unsigned i = 0; i < tamanho; i++) inicializaPagina(&(fila->paginas[i]));

	fila->final = 0;

	return fila;

}

void insereFila (Fila *fila, Pagina *pagina, _Bool referenciar) {

	fila->paginas[fila->final].indiceTabela = pagina->indiceTabela; 
	fila->paginas[fila->final].paginaVirtual = pagina->paginaVirtual; 
	fila->paginas[fila->final].moldura = pagina->moldura; 
	fila->paginas[fila->final].indiceFila = fila->final; 
	fila->paginas[fila->final].referenciado = referenciar; 

	fila->final++;
}

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

unsigned removeFila (Fila *fila, unsigned posicao) {

	unsigned moldura = fila->paginas[posicao].moldura;

	for (unsigned i = posicao; i < fila->final-1; i++){
	
		fila->paginas[i] = fila->paginas[i+1];
		fila->paginas[i].indiceFila--;

	}

	fila->final--;

	return moldura;

}

void imprimeFila(Fila *fila){

	printf("\nFila sg:\n");

	for(unsigned i = 0; i < fila->final; i++){
		printf("[pv: %d - i: %d - r: %d] -> ",fila->paginas[i].paginaVirtual, fila->paginas[i].indiceTabela, fila->paginas[i].referenciado);
	}
	printf("||\n\n");

}