#include "compilador.h"

int main (int argc, char **argv) {

    //FILE *saida = fopen("tokens.dat", "r");
    char *entrada = carregaPrograma(argv[1]);
    int numSimbolos = 0, r;
    ListaTokens *lista = criaLista(), *erros = criaLista();
    
    TabelaSimbolos tabelaSimbolos;
    tabelaSimbolos.simbolos = NULL;
    tabelaSimbolos.tamanho = 0;
    //char **tokenTable = carregaTokens();

    r = analiseLexica(entrada, lista, erros);
    
    if (r != 0){
        printf("--> Erros Léxicos:\n");
        printListaToken(erros);
        getchar();
    }
    printf("--> Análise Léxica:\n");
    printListaToken(lista);
    getchar();

    if (constroiTabelaSimbolos(lista, &tabelaSimbolos) == 0) {
        printf("--> Número de símbolos: %d\n", tabelaSimbolos.tamanho);
        for (int i = 0; i < tabelaSimbolos.tamanho; i++) {
            printf("Identificador: %s\n", tabelaSimbolos.simbolos[i].valor);
        }
        printf("Número de símbolos: %d\n", tabelaSimbolos.tamanho);
    } else{
        printf("Nenhum símbolo encontrado");
    }
    printf("\n");
    getchar();

    r = analiseSintatica(lista, erros, &tabelaSimbolos);

    printTabelaSimbolos(tabelaSimbolos);
    getchar();
    printListaToken(erros);

    free(entrada);
    liberaLista(lista);
    liberaLista(erros);

    return 0;
}