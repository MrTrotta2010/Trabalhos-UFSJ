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
    
    char pivo, sentinela;
    ListaTokens listaTokens;

    regex_t coment;
    regcomp(&coment, "/*.*/", int cflags);

    for (int i = 0; i < strlen(codigo); i++) {

        pivo = codigo[i];
        printf("%c", pivo);
    }

    return listaTokens;
} 