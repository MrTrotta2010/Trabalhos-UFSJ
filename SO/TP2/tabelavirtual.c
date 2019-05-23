#include "tp2virtual.h"

void inicializaPagina(Pagina *pagina){

	pagina->mudou = FALSE;
	pagina->valido = FALSE;
	pagina->referenciado = FALSE;
	pagina->paginaVirtual = -1;
	pagina->moldura = -1;
	pagina->indiceFila = -1;
	pagina->prox = NULL;
}

Pagina * criaPagina(){

	Pagina *pagina = (Pagina *) malloc(sizeof(Pagina));

	inicializaPagina(pagina);

	return pagina;
}

TabelaPagina inicializaTabela(Configuracao *config){

	TabelaPagina tabPag;

	tabPag.pagina = (Pagina *) malloc((config->tamMem/config->tamPag) * sizeof(Pagina));
	tabPag.statusMemoria = (_Bool *) malloc(config->tamMem/config->tamPag * sizeof(_Bool));
	tabPag.referenciado = (unsigned *) malloc(config->tamMem/config->tamPag * sizeof(unsigned));
	tabPag.moldurasUsadas = 0;
	tabPag.numMolduras = config->tamMem/config->tamPag;

	for(int i = 0; i < config->tamMem/config->tamPag; i++){

		tabPag.statusMemoria[i] = FALSE;
		tabPag.referenciado[i] = 0;
		inicializaPagina(&(tabPag.pagina[i]));
	}

	return tabPag;
}

int posicaoMemoria(TabelaPagina *tabelaPag){

	for(int i = 0; i < tabelaPag->numMolduras; i++){

		if(!(tabelaPag->statusMemoria[i]))
			return i;
	}

	return 0;
}
	
int PaginaVirtualQueTaNaMolduraQueVouLimparDaMemoria(Pagina *pagina, int moldura){
	if(pagina->moldura == moldura){
		return pagina->paginaVirtual;

	}
	return -1;
}

void copiaPagina(Pagina *pagDestino, Pagina *pagFonte){

	pagDestino->mudou = pagFonte->mudou;
	pagDestino->valido = pagFonte->valido;
	pagDestino->paginaVirtual = pagFonte->paginaVirtual;
	pagDestino->moldura = pagFonte->moldura;
	pagDestino->prox = pagFonte->prox;
	free(pagFonte);
}

unsigned retiraPagina(TabelaPagina *tabelaPag, Fila *filaPaginas, int substituicao) {

	unsigned escolhido = escolheMoldura(tabelaPag, filaPaginas, substituicao);
	
	if(debug) {
		foreground(YELLOW);
		printf("=> Moldura escolhida: %d\n", escolhido);	
		FORENORMAL_COLOR;	
	}	
	unsigned paginaVirtual;	

	tabelaPag->statusMemoria[escolhido] = FALSE;
	tabelaPag->moldurasUsadas--;

	Pagina *aux;

	for(int i = 0; i < tabelaPag->numMolduras; i++){

		aux = &(tabelaPag->pagina[i]);

		do{
			
			paginaVirtual = PaginaVirtualQueTaNaMolduraQueVouLimparDaMemoria(aux, escolhido);
			
			if(paginaVirtual != -1){
				
				if (aux->mudou) pagEscritas++;
				
				if (aux->mudou && aux->referenciado) tabelaPag->referenciado[escolhido] = 2;
				else if (aux->mudou && !aux->referenciado) tabelaPag->referenciado[escolhido] = 0;

				copiaPagina(aux, aux->prox);

				if(debug) {
					foreground(YELLOW);
					printf("=> Retirou a página virtual %d da memória (moldura %d)\n", paginaVirtual, escolhido);
					FORENORMAL_COLOR;
				}
				i = tabelaPag->numMolduras;

				break;
			}
			else{
				if(aux->prox != NULL)
					aux = aux->prox;
				else
					break;
			}


		}while(aux->moldura != -1);

	}
	return escolhido;
}


int isPageFault(TabelaPagina *tabelaPagina, Pagina *pagina, Fila *filaPaginas, int substituicao, unsigned paginaVirtual, unsigned clock, char rw){

	Pagina *paginaAtual = pagina;

	while(paginaAtual->paginaVirtual != -1){

		if(paginaAtual->paginaVirtual == paginaVirtual && paginaAtual->valido){

			paginaAtual->referenciado = TRUE;
			
			if(debug) {
				foreground(GREEN);
				printf("Page hit!\n");
				FORENORMAL_COLOR;
			}
			pageHit++;
			
			if(paginaAtual->mudou == FALSE) paginaAtual->mudou = (rw == 'W') ? TRUE : FALSE;

			switch (substituicao){

				case 0://lru
					tabelaPagina->referenciado[paginaAtual->moldura] = clock;
					break;

				case 1://nru
					tabelaPagina->referenciado[paginaAtual->moldura] = (paginaAtual->mudou) ? 3 : 2;
					break;

				case 2://segunda chance
					paginaAtual->referenciado = TRUE;
					reorganizaFila(filaPaginas, paginaAtual->indiceFila, TRUE);
					paginaAtual->indiceFila = filaPaginas->final - 1;
					//imprimeFila(filaPaginas);
					break;
			}

			return 0;

		}

		paginaAtual = paginaAtual->prox;
	
	}

	if(debug) {
		foreground(RED);
		printf("Page Fault: pagina %d não encontrada na memoria!\n", paginaVirtual);
		FORENORMAL_COLOR;
	}
	pageFault++;

	return 1;
}

int memCheia(TabelaPagina *tabelaPagina, long unsigned tamMemoria){

	return !(tabelaPagina->moldurasUsadas < tamMemoria);
}

void inserePagina(TabelaPagina *tabelaPag, Fila *filaPaginas, unsigned molduraVaga, int substituicao, unsigned clock, unsigned indiceTabela, char rw, unsigned paginaVirtual){

	tabelaPag->moldurasUsadas++;

	Pagina *paginaAtual = &(tabelaPag->pagina[indiceTabela]);

	while(paginaAtual->prox != NULL) paginaAtual = paginaAtual->prox;

	paginaAtual->mudou = (rw == 'W') ? TRUE : FALSE;
	paginaAtual->valido = TRUE;
	tabelaPag->statusMemoria[molduraVaga] = TRUE;
	paginaAtual->paginaVirtual = paginaVirtual;
	paginaAtual->moldura = molduraVaga;
	paginaAtual->indiceTabela = indiceTabela;
	paginaAtual->indiceFila = -1;
	paginaAtual->prox = criaPagina();

	switch(substituicao){
		
		case 0://lru
			tabelaPag->referenciado[paginaAtual->moldura] = clock;
			break;
		
		case 1://nru
			tabelaPag->referenciado[paginaAtual->moldura] = (paginaAtual->mudou) ? 3 : 2;
			break;

		case 2://segunda chance
			insereFila (filaPaginas, paginaAtual, TRUE);
		    break;

	}

	paginaAtual->indiceFila = filaPaginas->final - 1;
	
	
	pagLidas++;


	if(debug){
		foreground(YELLOW);
		printf("=> Inseriu a pagina na moldura %d da memória\n", paginaAtual->moldura);
		FORENORMAL_COLOR;
	} 
}