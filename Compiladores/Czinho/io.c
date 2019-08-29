#include "compilador.h"

char *carregaPrograma (char *arquivo) {

	FILE *entrada = fopen(arquivo, "r");
	char *buffer = NULL;
	unsigned long tamanho;

	if (entrada) {

		fseek(entrada, 0, SEEK_END);
		tamanho = ftell(entrada);
		fseek(entrada, 0, SEEK_SET);
		buffer = malloc(tamanho);
		fread(buffer, 1, tamanho, entrada);
		fclose(entrada);
	}

	return buffer;
}