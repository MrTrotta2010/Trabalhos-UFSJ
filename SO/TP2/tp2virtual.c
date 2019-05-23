#include "tp2virtual.h"

//desaloca a estrutura fila, utilizada no algoritmo segunda_chance
void freeFila(Fila *fila){

	free(fila->paginas);
	free(fila);	
}

int main (int argc, char **argv){

	pagLidas = pagEscritas = pageHit = pageFault = 0;
	
	char rw;
	unsigned paginaVirtual;
	unsigned indiceTabela;
	unsigned enderecoAtual;
	unsigned molduraVaga;
	unsigned clock = 1;
	
	//inicializa as estruturas
	Configuracao *config = recebeConfig(argc, argv);
	Fila *filaPaginas = criaFila (config->tamMem / config->tamPag);
	TabelaPagina tabelaPag = inicializaTabela(config);

	debug = config->debug;

	system("clear");
	printf("\n>> Executando o simulador...\n");

	FILE *arqEntrada = fopen(config->arqEntrada, "r");

	if(debug) printTabela(&tabelaPag, "Tabela Inicial", 0);
	if(debug) printMemoria(&tabelaPag, "Memória Inicial", 0);

	while(!feof(arqEntrada)){
		
		fscanf(arqEntrada, "%x %c\n", &enderecoAtual, &rw);
		
		paginaVirtual = enderecoAtual / config->tamPag;
		
		indiceTabela = paginaVirtual % (config->tamMem / config->tamPag);
		
		if(debug){
			foreground(CYAN);
			printf("-----------------------------------------------------------------\n");
			FORENORMAL_COLOR;
			printf("\n=> Endereço: %x\n=> Na pagVirtual %d\n=> indice na Tabela %d %c\n\n", enderecoAtual, paginaVirtual, indiceTabela,rw);
		} 

		//verifica se a página está na memoria
		if(isPageFault(&tabelaPag, &(tabelaPag.pagina[indiceTabela]), filaPaginas, config->substituicao, paginaVirtual, clock, rw)){

			//caso page fault, verifica-se se há espaço na memória
			if(memCheia(&tabelaPag, (config->tamMem / config->tamPag))){

				if(debug) printMemoria(&tabelaPag, "Memória Cheia", 1);

				//caso memória cheia, retira-se uma pagina ta tabela e retorna a moldura em que ela estava na memória
				molduraVaga = retiraPagina(&tabelaPag, filaPaginas, config->substituicao);
					
				if(debug) printTabela(&tabelaPag, "Retirou uma página", 1);
				if(debug) printMemoria(&tabelaPag, "Memória atualizada", 0);
			}
			else//caso haja espaço na memória, então o retornamos
				molduraVaga = posicaoMemoria(&tabelaPag);
			
			//insere-se a página na tabela
			inserePagina(&tabelaPag, filaPaginas, molduraVaga, config->substituicao, clock, indiceTabela, rw, paginaVirtual);

			if(debug) printTabela(&tabelaPag, "Inseriu a página", 0);
			if(debug) printMemoria(&tabelaPag, "Memória atualiza", 0);

		}

		//lru
		clock++;

		//nru
		if(config->substituicao == 1 && (clock % (config->tamMem/config->tamPag)) == 0) resetaReferenciado(&tabelaPag);
		
		if(debug) getchar();
	}

	imprimeLog(config, pagLidas, pagEscritas);

	free(config);
	freeFila(filaPaginas);

	return 0;

}