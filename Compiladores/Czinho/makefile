all:	gccinho

gccinho:	compilador.o	lexico.o	io.o
	gcc	-g compilador.o	lexico.o	io.o	-o	gccinho

compilador.o:	compilador.c	lexico.c	io.c
	gcc	-c -g	-Wall	compilador.c
	gcc	-c -g	-Wall	lexico.c
	gcc	-c -g -Wall	io.c

clean:
	rm compilador.o	gccinho.o	lexico.o	io.c	gccinho