#include <stdio.h>


void addchar(char c)
{
    static int counter = 0;
    static char saved;
    if ((c != '!') && (c != '?') && (c != '.')) {
        return;
    }
    if (counter == 0) {
        saved = c;
        counter = 1;
        return;
    } else {
        counter = 0;
        if (saved == '.') {
            if (c == '.') {
                putchar('+');
                return;
            } else if (c == '!') {
                putchar(',');
                return;
            } else if (c == '?') {
                putchar('>');
                return;
            }
        } else if (saved == '!') {
            if (c == '.') {
                putchar('.');
                return;
            } else if (c == '!') {
                putchar('-');
                return;
            } else if (c == '?') {
                putchar('[');
                return;
            }
        } else if (saved == '?') {
            if (c == '.') {
                putchar('<');
                return;
            } else if (c == '!') {
                putchar(']');
                return;
            }
        }
    }
}

int main (void)
{
    int c;
    while ((c = getchar()) != EOF)  {
        addchar(c);
    } 
    putchar('\n');
}
