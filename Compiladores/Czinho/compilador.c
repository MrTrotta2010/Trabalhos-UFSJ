#include "compilador.h"

int main (int argc, char **argv) {

    //FILE *saida = fopen("tokens.dat", "r");
    char *entrada = carregaPrograma(argv[1]);
    //char **tokenTable = carregaTokens();

    ListaTokens *lista = analiseLexica(entrada);
    printListaToken(lista);

    free(entrada);
    liberaLista(lista);

    return 0;
}