#include "tp2virtual.h"

Configuracao* recebeConfig(int numArg, char **argv){

	Configuracao *config = (Configuracao*) malloc(sizeof(Configuracao));

	if (numArg != 5 && numArg != 6) {
		printf("Argumentos Inválidos!\n");
		exit(1);
	}

	strcpy(config->nomeSubstituicao, argv[1]);

	if(strcmp(argv[1], "lru") == 0){
		config->substituicao = 0; 
	}
	else if(strcmp(argv[1], "nru") == 0){
		config->substituicao = 1; 
	}
	else if(strcmp(argv[1], "segunda_chance") == 0){
		config->substituicao = 2; 
	}
	else {
		printf("Algoritmo de substituicao inválido!\n");
		exit(1);
	}

	FILE *arqEntrada = fopen(argv[2], "r");

	if(arqEntrada != NULL){
		strcpy(config->arqEntrada, argv[2]);
		fclose(arqEntrada);
	}
	else{
		printf("Arquivo %s inexistente!\n", argv[2]);
		exit(1);
	}

	config->tamMem = atoi(argv[4]) * KB;

	if(config->tamMem <= 0){
		printf("Tamanho de memória inválido!\n");
		exit(1);
	}

	config->tamPag = atoi(argv[3]) * KB; 

	if(config->tamPag <= 0 || config->tamMem % config->tamPag != 0){
		printf("Tamanho de página inválido!\n");
		exit(1);
	}

	config->debug = (numArg == 6) ? atoi(argv[5]) : 0;

	return config;
}


void imprimeLog(Configuracao *config, unsigned pagLidas, unsigned pagEscritas){
	
	printf("\nSimulação finalizada\n");
	printf("Algoritmo de substituição: %s\n", config->nomeSubstituicao);
	printf("Arquivo de entrada: %s\n", config->arqEntrada);
	printf("Tamanho da memoria: %d KiB\n", config->tamMem);
	printf("Tamanho das paginas: %d KiB\n", config->tamPag);
	printf("Páginas lidas: %d\n", pagLidas);
	printf("Páginas escritas: %d\n", pagEscritas);
	printf("Page Hits: %d\n", pageHit);
	printf("Page Faults: %d\n", pageFault);
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

