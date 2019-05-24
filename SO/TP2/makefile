all:	tp2virtual

tp2virtual:	tp2virtual.o	io.o	fila.o	tabelavirtual.o	substituicao.o
	gcc	tp2virtual.o	io.o	fila.o	tabelavirtual.o	substituicao.o	-o	tp2virtual

tp2virtual.o:	tp2virtual.c	io.c	fila.c	tabelavirtual.c	substituicao.c
	gcc	-c	-g	-Wall	tp2virtual.c
	gcc -c	-g	-Wall	io.c
	gcc -c	-g	-Wall	fila.c
	gcc -c	-g	-Wall	tabelavirtual.c
	gcc -c	-g	-Wall	substituicao.c
	
clean:
	rm	tp2virtual	io.o	fila.o	tp2virtual.o	tabelavirtual.o	substituicao.o