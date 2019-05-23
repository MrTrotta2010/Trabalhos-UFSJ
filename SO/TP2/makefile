all:	tp2virtual

tp2virtual:	tp2virtual.o	io.o	fila.o
	gcc	tp2virtual.o	io.o	fila.o	-o	tp2virtual

tp2virtual.o:	tp2virtual.c	io.c	fila.c
	gcc	-c	-g	-Wall	tp2virtual.c
	gcc -c	-g	-Wall	io.c
	gcc -c	-g	-Wall	fila.c
	
clean:
	rm tp2virtual.o	io.o	fila.o	tp2virtual