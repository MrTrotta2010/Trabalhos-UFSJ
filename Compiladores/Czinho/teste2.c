#include <stdio.h>
#include<string.h>

#define TRUE 1
#define FALSE 0

int main () {

    int vetor[5] = {0, 1, 2, 3, 4};

    for (int i=0; i<=5; i++) {

        if (vetor[i] > 2) {
            puts("É maior!");
            vetor[i] *= 0.5;
        }
    }

    int a = TRUE, b = FALSE;

    if (a || b) a = b;
    if (!(a && b)) a = b = !b;

    return 0;
}