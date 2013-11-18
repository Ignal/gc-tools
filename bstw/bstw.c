#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int cval(int ch) {
    ch = toupper(ch);
    if ((ch >= 'A') && (ch <= 'Z')) {
        return ch - 'A' + 1;
    }
    if ((ch >= '0') && (ch <= '9')) {
        return ch - '0';
    }
    return 0;
}

int main (int argc, char** argv)
{
    int sum = 0;
    int len = 0;
    int n = 0;
    if (argc < 2) {
        int ch;
        while (!feof(stdin)) {
            sum += cval(fgetc(stdin));
        }
    } else {
        int arg = 1;
        for (; arg < argc; ++arg) {
            len = strlen(argv[arg]);
            for (n = 0; n < len; ++n) {
                sum += cval(argv[arg][n]);
            }
        }
    }
    printf("%d\n", sum);
    exit(EXIT_SUCCESS);
}
