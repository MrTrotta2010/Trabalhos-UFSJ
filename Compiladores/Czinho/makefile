all:	gccinho

gccinho:	compilador.o	lexico.o	io.o
	gcc	compilador.o	lexico.o	io.o	-o	gccinho

compilador.o:	compilador.c	lexico.c	io.c
	gcc	-c	-Wall	compilador.c
	gcc	-c	-Wall	lexico.c
	gcc	-c	-Wall	io.c

clean:
	rm compilador.o	gccinho.o	lexico.o	io.c	gccinho