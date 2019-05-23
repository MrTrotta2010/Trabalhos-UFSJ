#include "tp2virtual.h"

unsigned lru(TabelaPagina * tabelaPagina){

	int lru = tabelaPagina->referenciado[0];
	int moldura = 0;
	
	for(int i = 0; i < tabelaPagina->numMolduras; i++){
	
		if(tabelaPagina->referenciado[i] < lru){
	
			lru = tabelaPagina->referenciado[i];
			moldura = i;
		}
	}
	
	return moldura;
}

unsigned nru(TabelaPagina *tabelaPagina){

	unsigned um = -1, dois = -1, tres = -1;

	for(unsigned i = 0; i < tabelaPagina->numMolduras; i++ ){
		
		if (tabelaPagina->referenciado[i] == 0) return i;

		else {

			if (tabelaPagina->referenciado[i] == 1 && um == -1) um = i;

			else if (tabelaPagina->referenciado[i] == 2 && dois == -1 && um == -1) dois = i;

			else if (tabelaPagina->referenciado[i] == 3 && tres == -1 && um == -1 && dois == -1) tres = i;

		}
	}

	if (um != -1) return um;
	if (dois != -1) return dois;

	return tres;

}

unsigned segundaChance(TabelaPagina *tabelaPagina, Fila *filaPaginas){
	
	unsigned escolhido;

	for(unsigned i = 0; i < filaPaginas->final; i++){

		if(!(filaPaginas->paginas[i].referenciado)){
			
			escolhido = removeFila(filaPaginas, i);

			return escolhido;
		}

		else {

			reorganizaFila(filaPaginas, i, FALSE);
			i--;
		}
	}

	return 0;

}

unsigned escolheMoldura(TabelaPagina *tabelaPagina, Fila *filaPaginas, int substituicao){

	unsigned escolhido;
	
	switch(substituicao){
		case 0:
			escolhido = lru(tabelaPagina);
			break;
		case 1:
			escolhido = nru(tabelaPagina);
			break;
		case 2:
			escolhido = segundaChance(tabelaPagina, filaPaginas);
			break;
	}

	return escolhido;
}

void resetaReferenciado(TabelaPagina *tabelaPagina){
	
	for(int i = 0; i < tabelaPagina->numMolduras; i++ ){

		switch(tabelaPagina->referenciado[i]){
			case 2:
				tabelaPagina->referenciado[i] = 0;
				break;

			case 3:
				tabelaPagina->referenciado[i] = 1;
				break;
		} 
	}
}