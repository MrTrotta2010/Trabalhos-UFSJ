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

void copyPagina(Pagina *pagDestino, Pagina *pagFonte){

	pagDestino->mudou = pagFonte->mudou;
	pagDestino->valido = pagFonte->valido;
	pagDestino->paginaVirtual = pagFonte->paginaVirtual;
	pagDestino->moldura = pagFonte->moldura;
	pagDestino->prox = pagFonte->prox;
	free(pagFonte);
}

void printTabela(TabelaPagina *tabelaPag, char titulo[256], int cor){

	if(cor) foreground(RED);
	else foreground(BLUE);

	if(titulo[0] != '0') printf("\n -- %s -- \n", titulo);
	printf("\n");
	
	FORENORMAL_COLOR;
	Pagina *j;

	for(int i = 0; i < tabelaPag->numMolduras; i++){

		printf("|%d|-> ", i);

		for(j = &(tabelaPag->pagina[i]); j->moldura != -1; j = j->prox){
			
			printf("[pV: %d - md: %d - i: %d]-> ", j->paginaVirtual, j->moldura, j->indiceFila);

		}
		printf("[vazio]-> null\n");

	}

}

void printMemoria(TabelaPagina *tabelaPag, char titulo[256], int cor){

	if(cor) foreground(RED);
	else foreground(BLUE);

	if(titulo[0] != '0') printf("\n-- %s --\n", titulo);
	FORENORMAL_COLOR;

	printf("\n[");

	for(int i = 0; i < tabelaPag->numMolduras; i++){

		printf("%3d",tabelaPag->statusMemoria[i]);

	}
	printf(" ]\n\n");
	//d();
}


int lru(TabelaPagina * tabelaPagina){

	int lru = tabelaPagina->referenciado[0];
	int moldura = 0;
	
	for(int i = 0; i < tabelaPagina->numMolduras; i++){
	
		if(tabelaPagina->referenciado[i] < lru){
	
			lru = tabelaPagina->referenciado[i];
			moldura = i;
		}
	}
	
	return moldura;
}

unsigned nru(TabelaPagina *tabelaPagina){

	unsigned um = -1, dois = -1, tres = -1;

	for(unsigned i = 0; i < tabelaPagina->numMolduras; i++ ){
		
		if (tabelaPagina->referenciado[i] == 0) return i;

		else {

			if (tabelaPagina->referenciado[i] == 1 && um == -1) um = i;

			else if (tabelaPagina->referenciado[i] == 2 && dois == -1 && um == -1) dois = i;

			else if (tabelaPagina->referenciado[i] == 3 && tres == -1 && um == -1 && dois == -1) tres = i;

		}
	}

	if (um != -1) return um;
	if (dois != -1) return dois;

	return tres;

}



unsigned segundaChance(TabelaPagina *tabelaPagina, Fila *filaPaginas){
	
	unsigned escolhido;

	for(unsigned i = 0; i < filaPaginas->final; i++){

		if(!(filaPaginas->paginas[i].referenciado)){
			
			escolhido = removeFila(filaPaginas, i);

			return escolhido;
		}

		else {

			reorganizaFila(filaPaginas, i, FALSE);
			i--;
		}
	}

	return 0;

}

unsigned escolheMoldura(TabelaPagina *tabelaPagina, Fila *filaPaginas, int substituicao){

	unsigned escolhido;
	
	switch(substituicao){
		case 0:
			escolhido = lru(tabelaPagina);
			break;
		case 1:
			escolhido = nru(tabelaPagina);
			break;
		case 2:
			escolhido = segundaChance(tabelaPagina, filaPaginas);
			break;
	}

	return escolhido;
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

				copyPagina(aux, aux->prox);

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

void resetaReferenciado(TabelaPagina *tabelaPagina){
	
	for(int i = 0; i < tabelaPagina->numMolduras; i++ ){

		switch(tabelaPagina->referenciado[i]){
			case 2:
				tabelaPagina->referenciado[i] = 0;
				break;

			case 3:
				tabelaPagina->referenciado[i] = 1;
				break;
		} 
	}
}


int main (int argc, char **argv){

	pagLidas = pagEscritas = pageHit = pageFault = escritasDisco = 0;
	
	char rw;
	unsigned paginaVirtual;
	unsigned indiceTabela;
	unsigned enderecoAtual;
	unsigned molduraVaga;
	unsigned clock = 1;
	
	Configuracao *config = recebeConfig(argc, argv);
	Fila *filaPaginas = criaFila (config->tamMem / config->tamPag);
	TabelaPagina tabelaPag = inicializaTabela(config);

	debug = config->debug;

	printf("\nExecutando o simulador...\n");

	FILE *arqEntrada = fopen(config->arqEntrada, "r");

	if(debug) printTabela(&tabelaPag, "Tabela Inicial", 0);
	if(debug) printMemoria(&tabelaPag, "0", 1);

	while(!feof(arqEntrada)){
		
		fscanf(arqEntrada, "%x %c\n", &enderecoAtual, &rw);
		
		paginaVirtual = enderecoAtual / config->tamPag;
		
		indiceTabela = paginaVirtual % (config->tamMem / config->tamPag);
		
		if(debug){
			foreground(YELLOW);
			printf("=> Endereço: %x\n=> Na pagVirtual %d\n=> indice na Tabela %d %c\n", enderecoAtual, paginaVirtual, indiceTabela,rw);
			FORENORMAL_COLOR;
		} 

		if(isPageFault(&tabelaPag, &(tabelaPag.pagina[indiceTabela]), filaPaginas, config->substituicao, paginaVirtual, clock, rw)){

			if(memCheia(&tabelaPag, (config->tamMem / config->tamPag))){

				if(debug) printMemoria(&tabelaPag, "Memória Cheia", 1);

				molduraVaga = retiraPagina(&tabelaPag, filaPaginas, config->substituicao);
					
				if(debug) printTabela(&tabelaPag, "Retirou uma página", 1);
				if(debug) printMemoria(&tabelaPag, "Memória atualizada", 0);
			}
			else
				molduraVaga = posicaoMemoria(&tabelaPag);
			
			inserePagina(&tabelaPag, filaPaginas, molduraVaga, config->substituicao, clock, indiceTabela, rw, paginaVirtual);

			if(debug) printTabela(&tabelaPag, "Inseriu a página", 0);
			if(debug) printMemoria(&tabelaPag, "Memória atualiza", 0);

		}

		clock++;

		if(config->substituicao == 1 && (clock % (config->tamMem/config->tamPag)) == 0) resetaReferenciado(&tabelaPag);
	}

	imprimeLog(config, pagLidas, pagEscritas);

}
