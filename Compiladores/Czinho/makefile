all:	gccinho

gccinho:	compilador.o	lexico.o	io.o	lista.o
	gcc	-g compilador.o	lexico.o	io.o	lista.o	-o	gccinho

compilador.o:	compilador.c	lexico.c	io.c	lista.c
	gcc	-c -g	-Wall	compilador.c
	gcc	-c -g	-Wall	lexico.c
	gcc	-c -g	-Wall	io.c
	gcc	-c -g	-Wall	lista.c

clean:
	rm compilador.o	gccinho.o	lexico.o	io.c	lista.o	gccinho