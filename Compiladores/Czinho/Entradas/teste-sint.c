#include <stdio.h>

float func(int a, int b);

int main (
    int a;
    int b;
    int c;
    b = 3;
    a = b * 2;
    c = func(a, b);
    return 0;
}

float func(int a, int b) {
    return a + b;
}