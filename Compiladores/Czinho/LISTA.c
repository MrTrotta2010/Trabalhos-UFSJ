//-----------------CÓDIGO DO ARQ.H--------------------------------//
struct token{
	char name[256];
	int id;
	int value;
	int line, column;
};

typedef struct token Token;
typedef struct element *TkList;

//-----------------CÓDIGO DO ARQ.C--------------------------------//

struct element{
	Token tk;
	struct element *prox;
};

typedef struct element Elem;

TkList* criaLista(){

	TkList* tkl = (TkList*) malloc(sizeof(TkList));
	if(tkl != NULL) *tkl = NULL;
	return tkl;
}

void liberaLista(TkList* tkl){

	if(tkl != NULL){
		Elem* no;

		while((*tkl) != NULL){
			no = *tkl;
			*tkl = (*tkl)->prox;
			free(no);
		}
		free (tkl);
	}	
}

int insereToken(TkList *tkl, Token tk){
	
	if(tkl == NULL) return FALSE;
	
	Elem *no = (Elem*) malloc(sizeof(Elem));
	if(no ==  NULL) return FALSE;
	
	no->tk = tk;
	no->prox = NULL;
	
	if((*tkl) ==  NULL) *tkl = no;
	
	else{
		
		Elem *aux = *tkl;
		while(aux->prox != NULL) aux = aux->prox;

		aux->prox = no;
	}
	return TRUE;
}

int printListaToken(TkList* tkl){

	if(tkl == NULL) return FALSE;
	if(*tkl == NULL) return FALSE;
	
	Elem *aux = *tkl;

	while(aux != NULL){
		printf("Name: %s\nId: %i\n", aux->tk.name, aux->tk.id);
		aux = aux->prox;
	}
	getchar();
	getchar();
	return TRUE;
}