#include "compilador.h"

int main (int argc, char **argv) {

    int linha = 0, coluna = 0;
    char pivo, sentinela;

    //FILE *saida = fopen("tokens.dat", "r");
    char *entrada = carregaPrograma(argv[1]);
    char **tokenTable = carregaTokens();

    ListaTokens lista;

    // printf ("Tokens:\n");
    // for (int i = 0; i < NUM_TOKENS; i++)
    //     printf ("\t%s\n", tokenTable[i]);

    //lista = analiseLexica(entrada);

    free(entrada);
    for (int i = 0; i < NUM_TOKENS; i++)
        free(tokenTable[i]);
    free(tokenTable);

    return 0;
}