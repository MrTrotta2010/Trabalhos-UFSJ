#include "shellso.h"

_Bool entradaVazia(char* input){
	if(strcmp(input, "\n") == 0 || strcmp(input, "\0") == 0){
	//retorna um código pra função que chamou, informando a entrada vazia
		return 1
	}
	return 0;
}


_Bool fim(char *input){
	if(strcmp(input, "fim\n") == 0){
		return 1;
	}
	return 0;
}

int numArgs(char * input){
	
	int argc = 1, i;

	for(i = 0; i < strlen(input); i++){
		if(input[i] == ' '){
			argc++;
		}
	}
	return argc;
}

int numProcess(char * input){
	int argc = 1, i;

	for(i = 0; i < strlen(input); i++){
		if(input[i] == '|'){
			argc++;
		}
	}
	return argc;
}

char *** interpretaEntrada(char *input){

	char ***argv, *token;

	// verificar entrada vazia
	if(entradaVazia(input)){
		return NULL;
	}

	// verifica comando de término do shell
	if(fim(input)){
		// mata o shell
		exit(EXIT_SUCCESS);		
	}

	//aloca um vetor de vetor de argumentos (cada posição é um vetor de argumento pra um processo que será criado)
	argv = (char***) malloc(numProcess(input) * sizeof(char**));

	//token recebe o primeiro argumento
    token = strtok(input, " ");

    //pra cada processo, preenche seu argv
	for(int j = 0; j < numProcess(input); j++){

		//aloca o vetor de argumento do processo j
		//TODO: tá alocando memória desnecessária aqui
		argv[j] = (char**) malloc(numArgs(input) * sizeof(char*));

	    //copia os argumentos do processo j pro argv[j]
	    for(short argc = 0; token != NULL && token != '|'; argc++) {
	        argv[j][argc] = (char*) malloc(strlen(token) * sizeof(char));
	        strcpy(argv[j][argc], token);
	        token = strtok(NULL, " ");
	    }

	    //caso a string termine com a quebra de linha, a retira para corrigir o argumento
	    if(argv[argc-1][strlen(argv[argc-1])-1] == '\n'){
	    	argv[argc-1][strlen(argv[argc-1])-1] = '\0';
	   	}

	   	//ultima posição do vetor de argumentos aponta para NULL, para indicar fim dos argumentos
	   	argv[j][argc] = NULL;
	}

	return argv;
}

void readInputFile(FILE *file, char *input){
	
	if(!feof(file)){
		fgets(input, 1023, file);
	}
	else{
		fclose(file);
		exit(EXIT_SUCCESS);
	}
}

FILE * openFile(char *arg){

	FILE *file = fopen(arg, "r");
	
	if(file == NULL){
		printf("Arquivo %s inexistente!\n", arg);
		exit(EXIT_FAILURE);
	}
	return file;
}

void readInputStdin(char *input){
	fgets(input, 1023, stdin);
}

void prompt(){
	printf("Sim, mestre? ");	
}
