all:	gccinho

gccinho:	compilador.o	lexico.o	sintatico.o	io.o	lista.o
	gcc	-g compilador.o	lexico.o	sintatico.o	io.o	lista.o	-o	gccinho

compilador.o:	compilador.c	lexico.c	sintatico.o	io.c	lista.c
	gcc	-c -g	-Wall	compilador.c
	gcc	-c -g	-Wall	lexico.c
	gcc	-c -g	-Wall	sintatico.c
	gcc	-c -g	-Wall	io.c
	gcc	-c -g	-Wall	lista.c

clean:
	rm compilador.o	gccinho.o	lexico.o	sintatico.o	io.c	lista.o	gccinho