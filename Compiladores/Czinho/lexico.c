#include "compilador.h"

char **carregaTokens() {

    FILE *entrada = fopen("tokens.table", "r");
    assert(entrada);

    char *linha = NULL;
    size_t len = 0;
    ssize_t read;
    int i = 0, lixo;

    char **tokens = malloc(NUM_TOKENS*sizeof(char*));

    while ((read = getline(&linha, &len, entrada)) != -1) {

        tokens[i] = malloc(30*sizeof(char));
        sscanf(linha, "%d %s\n", &lixo, tokens[i]);
        i++;
    }

    fclose(entrada);

    return tokens;
}

ListaTokens analiseLexica (char *codigo) {
    
    int pivo = 0, sentinela, posicaoPal;
    ListaTokens listaTokens;
	char *caractere = NULL, palavra[256];

	regex_t coment;
	regcomp(&coment, "/\*.\*/", REG_EXTENDED|REG_NOSUB);
    regex_t alfa;
	regcomp(&alfa, "[a-zA-Z]", REG_EXTENDED|REG_NOSUB);
    regex_t separador;
	regcomp(&separador, "[/s;,]", REG_EXTENDED | REG_NOSUB);

	while (pivo < strlen(codigo)) {

        *caractere = codigo[pivo];
		sentinela = pivo;
		posicaoPal = 0;
		//printf("%c", pivo);

		if ((regexec(&alfa, caractere, 0, (regmatch_t *)NULL, 0)) == 0) {

			while ((regexec(&separador, caractere, 0, (regmatch_t *)NULL, 0)) != 0) {
				sentinela++;
				palavra[posicaoPal] = *caractere;
				posicaoPal++;
			}

			printf("%s\n", palavra);

		} else
			printf("Não Casou\n");
    }

    return listaTokens;
} 