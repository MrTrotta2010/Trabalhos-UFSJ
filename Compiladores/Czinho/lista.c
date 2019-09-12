#include "compilador.h"

struct elemento{
	Token tk;
	struct elemento *prox;
};

typedef struct elemento Elemento;

ListaTokens* criaLista(){

	ListaTokens* tkl = (ListaTokens*) malloc(sizeof(ListaTokens));
	if(tkl != NULL) *tkl = NULL;
	return tkl;
}

void liberaLista(ListaTokens* tkl){

	if(tkl != NULL){
		Elemento* no;

		while((*tkl) != NULL){
			no = *tkl;
			*tkl = (*tkl)->prox;
			free(no);
		}
		free (tkl);
	}	
}

int insereToken(ListaTokens *tkl, Token tk){
	
	if(tkl == NULL) return FALSE;
	
	Elemento *no = (Elemento*) malloc(sizeof(Elemento));
	if(no ==  NULL) return FALSE;
	
	no->tk = tk;
	no->prox = NULL;
	
	if((*tkl) ==  NULL) *tkl = no;
	
	else{
		
		Elemento *aux = *tkl;
		while(aux->prox != NULL) aux = aux->prox;

		aux->prox = no;
	}
	return TRUE;
}

int printListaToken(ListaTokens *tkl){

	if(*tkl == NULL) {
		return FALSE;
	}

	Elemento *aux = *tkl;

	while(aux != NULL){
		printf("------------------------------------------------\n");
		printf("-> %d - %s: %s\n", aux->tk.id, aux->tk.classe, aux->tk.valor);
		printf("       Linha %d, coluna %d\n",aux->tk.linha, aux->tk.coluna);
		printf("------------------------------------------------\n");
		aux = aux->prox;
	}

	return TRUE;
}