#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
#include <errno.h>

char ** interpretaEntrada(char *input){

	short argc = 0;
	char **argv, *token;

	// verificar entrada vazia
	if(strcmp(input, "\n") == 0 || strcmp(input, "\0") == 0){
		//retorna um código pra função que chamou, informando a entrada vazia
		return NULL;
	}

	// verifica comando de término do shell
	if(strcmp(input, "fim\n") == 0){
		// retorna um código para a função que chamou, informando para matar o shell
		exit(EXIT_SUCCESS);
	}

	//conta a quantidade de parametros pra alocar o vetor de strings argv
	for(int i = 0; i < strlen(input); i++){
		if(input[i] == ' ') argc++;
	}

	argv = (char**) malloc(argc * sizeof(char*));

    token = strtok(input, " ");

    argc = 0;
    while (token != NULL) {
        argv[argc] = (char*) malloc( strlen(token) * sizeof(char));
        strcpy(argv[argc], token);
        token = strtok(NULL, " ");
        argc++;
    }
    argv[argc-1][strlen(argv[argc-1])-1] = '\0';
   	argv[argc] = NULL;

	return argv;
}



int main(int argc, char *argv[]){
	
	// variável que armazena a entrada 
	char input[1024];
	
	// variável que armazena os argumentos da entrada
	char **arguments;

	// variável que armazena o pid do processo filho
	pid_t pid;

	//caso entre no modo arquivo
	FILE *file;
	
	if(argc == 2){
		file = fopen(argv[1], "r");
		if(file == NULL){
			printf("Arquivo %s inexistente!\n", argv[1]);
			exit(EXIT_FAILURE);
		}
	}

    while(1){

  
		switch(argc){
			
			//modo interativo
			case 1:	
				// imprime o prompt
    			printf("$ ");

				// lê a entrada e a armazena na string input
				fgets(input, 1023, stdin);
				break;

			//modo arquivo
			case 2:
				
				if(!feof(file)){
					fgets(input, 1023, file);
				}
				else{
					fclose(file);
					exit(EXIT_SUCCESS);
				}
			break;
			
			default: printf("Argumentos inválidos\n");
		}

		// processa a entrada e retorna um vetor contendo os argumentos da entrada
		arguments = interpretaEntrada(input);
		//se a entrada for vazia, volta no loop
		if(arguments == NULL){
			continue;
		}

		// cria processo filho e verifica a ocorrência de erro
		if((pid = fork()) < 0){
			printf("erro ao criar o processo\n");
			continue;
		}
		
		// processo filho: altera a imagem do processo filho (executa o programa )
		if(pid == 0){
			if(execvp(arguments[0], arguments)== -1){
				perror("execvp");
			}
			exit(EXIT_SUCCESS);
		}

		// processo pai: espera o filho terminar
		else{
			wait(NULL);
		}
    }

    return 0;
}

