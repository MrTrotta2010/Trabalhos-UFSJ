#include "compilador.h"

char *carregaPrograma (char *arquivo) {

	FILE *entrada = fopen(arquivo, "r");
	char *buffer;
	unsigned long tamanho;

	if (entrada) {

		fseek(entrada, 0, SEEK_END);
		tamanho = ftell(entrada);
		fseek(entrada, 0, SEEK_SET);
		buffer = calloc(tamanho+1, sizeof(char));
		fread(buffer, 1, tamanho, entrada);
		fclose(entrada);

	} else {
		printf("Erro ao abrir o arquivo de entrada \"%s\"!\n", arquivo);
		exit(1);
	}

	return buffer;
}