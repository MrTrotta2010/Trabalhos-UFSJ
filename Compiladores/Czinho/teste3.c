#include<string.h>
//Essa função verifica o tamanho da string;
int func (char *word) {

    char a = 'a';
    /* if (strlen(word) < 10)
        return 1;
    else
        return 0; */

    int r;
    (strlen(word) < 10) ? r=1 : r=0;
    return r;
}