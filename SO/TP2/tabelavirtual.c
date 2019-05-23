#include "tp2virtual.h"

//inicializa uma página da tabela de páginas
void inicializaPagina(Pagina *pagina){

	pagina->mudou = FALSE;
	pagina->valido = FALSE;
	pagina->referenciado = FALSE;
	pagina->paginaVirtual = -1;
	pagina->moldura = -1;
	pagina->indiceFila = -1;
	pagina->prox = NULL;
}

//cria uma página
Pagina * criaPagina(){

	Pagina *pagina = (Pagina *) malloc(sizeof(Pagina));

	inicializaPagina(pagina);

	return pagina;
}

//cria e inicializa a tabela de página
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

//retorna uma posição vaga na memória
int posicaoMemoria(TabelaPagina *tabelaPag){

	for(int i = 0; i < tabelaPag->numMolduras; i++){

		if(!(tabelaPag->statusMemoria[i]))
			return i;
	}

	return 0;
}
	
//retorna a página virtual da pagina que será removida da tabela de páginas
int encontraMoldura(Pagina *pagina, int moldura){
	if(pagina->moldura == moldura){
		return pagina->paginaVirtual;

	}
	return -1;
}

//copia os atributos de uma página
void copiaPagina(Pagina *pagDestino, Pagina *pagFonte){

	pagDestino->mudou = pagFonte->mudou;
	pagDestino->valido = pagFonte->valido;
	pagDestino->paginaVirtual = pagFonte->paginaVirtual;
	pagDestino->moldura = pagFonte->moldura;
	pagDestino->prox = pagFonte->prox;
	free(pagFonte);
}

//remove uma página da tabela de páginas
unsigned retiraPagina(TabelaPagina *tabelaPag, Fila *filaPaginas, int substituicao) {

	//retorna um espaço vago na memória, de acordo com a política de substituição utilizada
	unsigned escolhido = escolheMoldura(tabelaPag, filaPaginas, substituicao);
	
	if(debug) {
		foreground(RED);
		printf("=> Moldura escolhida: %d\n", escolhido);	
		FORENORMAL_COLOR;	
	}

	unsigned paginaVirtual;

	//marca a posição da memória retornada como true	
	tabelaPag->statusMemoria[escolhido] = FALSE;
	tabelaPag->moldurasUsadas--;

	Pagina *aux;

	//procura pela página que será removida
	for(int i = 0; i < tabelaPag->numMolduras; i++){

		aux = &(tabelaPag->pagina[i]);

		do{
			
			//verifica se a pagina atual está na moldura que será removida
			paginaVirtual = encontraMoldura(aux, escolhido);
			
			//se diferente de -1, pagina encontrada!
			if(paginaVirtual != -1){
				
				if (aux->mudou) {
					foreground(MARGENTA);
					if(debug) printf(">> Pagina %d escrita no disco\n", paginaVirtual);					
					FORENORMAL_COLOR;
					pagEscritas++;
				}

				//nru
				if (aux->mudou && aux->referenciado) tabelaPag->referenciado[escolhido] = 2;
				else if (aux->mudou && !aux->referenciado) tabelaPag->referenciado[escolhido] = 0;

				//copia os atributos da proxima página para a página que será removida
				copiaPagina(aux, aux->prox);

				if(debug) {
					foreground(RED);
					printf("=> Retirou a página virtual %d da memória (moldura %d)\n", paginaVirtual, escolhido);
					FORENORMAL_COLOR;
				}

				//quebra os loops
				i = tabelaPag->numMolduras;
				break;
			}
			else{
				if(aux->prox != NULL)
					aux = aux->prox;
				else
					break;
			}

		//enquanto não chegar na ultima página da lista
		}while(aux->moldura != -1);

	}
	return escolhido;
}


//verifica se a página está na memória
int isPageFault(TabelaPagina *tabelaPagina, Pagina *pagina, Fila *filaPaginas, int substituicao, unsigned paginaVirtual, unsigned clock, char rw){

	Pagina *paginaAtual = pagina;

	while(paginaAtual->paginaVirtual != -1){

		//caso a pagina virtual lida for igual a alguma página virtual da tabela, então Page Hit
		if(paginaAtual->paginaVirtual == paginaVirtual && paginaAtual->valido){

			paginaAtual->referenciado = TRUE;
			
			if(debug) {
				foreground(GREEN);
				printf("=> Page hit!\n");
				FORENORMAL_COLOR;
			}
			pageHit++;
			
			if(paginaAtual->mudou == FALSE) paginaAtual->mudou = (rw == 'W') ? TRUE : FALSE;

			//altera o referenciado da página, conforme a política de substituição
			switch (substituicao){

				case 0://lru
					tabelaPagina->referenciado[paginaAtual->moldura] = clock;
					break;

				case 1://nru, o vetor de referenciado é utilizado para armazenar as classes de cada página
					tabelaPagina->referenciado[paginaAtual->moldura] = (paginaAtual->mudou) ? 3 : 2;
					break;

				case 2://segunda chance
					paginaAtual->referenciado = TRUE;
					//quando referenciada, a página deverá ir para o fim da fila 
					reorganizaFila(filaPaginas, paginaAtual->indiceFila, TRUE);
					paginaAtual->indiceFila = filaPaginas->final - 1;
					break;
			}

			return 0;

		}
		//percorrendo a tabela
		paginaAtual = paginaAtual->prox;
	
	}

	if(debug) {
		foreground(RED);
		printf("=> Page Fault: pagina %d não encontrada na memoria!\n", paginaVirtual);
		FORENORMAL_COLOR;
	}
	pageFault++;

	return 1;
}

//verifica se a memória está cheia
int memCheia(TabelaPagina *tabelaPagina, long unsigned tamMemoria){

	return !(tabelaPagina->moldurasUsadas < tamMemoria);
}

//insere uma página na tabela
void inserePagina(TabelaPagina *tabelaPag, Fila *filaPaginas, unsigned molduraVaga, int substituicao, unsigned clock, unsigned indiceTabela, char rw, unsigned paginaVirtual){

	//menos uma posição na memória
	tabelaPag->moldurasUsadas++;

	//iniciamos na primeira posição da lista na tabela de paginas
	Pagina *paginaAtual = &(tabelaPag->pagina[indiceTabela]);

	//percorre-se até a ultima posição
	while(paginaAtual->prox != NULL) paginaAtual = paginaAtual->prox;

	//seta os dados desta nova página
	paginaAtual->mudou = (rw == 'W') ? TRUE : FALSE;
	paginaAtual->valido = TRUE;
	tabelaPag->statusMemoria[molduraVaga] = TRUE;
	paginaAtual->paginaVirtual = paginaVirtual;
	paginaAtual->moldura = molduraVaga;
	paginaAtual->indiceTabela = indiceTabela;
	paginaAtual->indiceFila = -1;
	//aponta para uma página vazia, esta que aponta para null
	paginaAtual->prox = criaPagina();

	//altera o referenciado 
	switch(substituicao){
		
		case 0://lru
			tabelaPag->referenciado[paginaAtual->moldura] = clock;
			break;
		
		case 1://nru, altera a classe
			tabelaPag->referenciado[paginaAtual->moldura] = (paginaAtual->mudou) ? 3 : 2;
			break;

		case 2://segunda chance, a casa inserção na tabela, insere-se também na fila
			insereFila (filaPaginas, paginaAtual, TRUE);
			//segunda_chance
			paginaAtual->indiceFila = filaPaginas->final - 1;
		    break;

	}

	pagLidas++;

	if(debug){
		foreground(GREEN);
		printf("=> Inseriu a pagina na moldura %d da memória\n", paginaAtual->moldura);
		FORENORMAL_COLOR;
	} 
}