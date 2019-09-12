# GCCINHO - Mini compilador de C

Trabalho desenvolvido na disciplina de Compiladores do curso de baixarelado em Ciência da Computação da UFSJ.
Por Tiago Trotta, setembro de 2019.

Para instalar:
- sudo apt-install git

Instruções para compilar e executar:
- Para compilar: $ make
- Para executar: $ ./gccinho <arquivo em c>

Limitações:
- Possui, ainda, somente o analisador léxico;
- Reconhece uma variedade muito pequena de erros léxicos;
- Não aponta a posição correta das palavras
- Podem haver bugs ainda não catalogados.

Uma entrada do tipo:
int func (int a) {
    a *= a;
    return a;
}

Resultará numa lista de tokens do tipo:
0 - RESERVADA: int
    Linha 1, coluna 1

1 - IDENTIFICADOR: func
    Linha 1, coluna 5
    
6 - SEPARADOR: (
    Linha 1, coluna 10
    
0 - RESERVADA: int
    Linha 1, coluna 11
(...)

A lista de tokens será exibida no terminal, seguindo o padrão:
ID - CLASSE: valor
    Linha i, coluna j

Licença: me siga no soundcloud e no youtube.
