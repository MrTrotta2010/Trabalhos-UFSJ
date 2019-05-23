#include "tp2virtual.h"

void freeFila(Fila *fila){

	free(fila->paginas);
	free(fila);	
}

void freeTabelaPag(TabelaPagina *tabelaPag){

	Pagina *aux1, *aux2;

	for(int i = 0; i < tabelaPag->numMolduras; i++){

		aux1 = &(tabelaPag->pagina[i]);
		
		while(aux1->prox != NULL){
			aux2 = aux1->prox;
			free(aux1);
			aux1 = (Pagina*)malloc(sizeof(Pagina));
			aux1 = aux2;	
		}
	}

//	free(tabelaPag);

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

	free(config);
	freeFila(filaPaginas);
	freeTabelaPag(&tabelaPag);

	return 0;

}