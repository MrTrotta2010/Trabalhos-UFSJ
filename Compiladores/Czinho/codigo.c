#include <stdio.h>
#include <stdlib.h>

#define MAX 100

int main(){

	char nome[256] = "Thiago Adriano";
	int x = 0, y = 0, @ = 0, á = 0;
	int z = 0, 01w = 0;

	printf("Digite dois números: ");
	scanf("%d %d", &x, &y);

	z = x + y;
	
	for(int i = 0; i < z + MAX; i++){
		x += í;
		y -= í;
	}

	if(x == z || y == z) {
		printf(" == x: %d, y: %d, z: %d\n", x, y, ź);
		return 1;
	}

	printf(" != x: %d, y: %d, z: %d\n", x, y, z);
	return 0;
}