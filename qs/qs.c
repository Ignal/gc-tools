#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void usage (void)
{
    fprintf(stderr, "usage: qs [-i] <Wert>\n");
    exit(1);
}


int qsn (int n)
{
    int m = 0;
    if (n <= 9) {
       return n;
    }
    while(n > 0) {
        m += n % 10;
        n /= 10;
    }
    return qsn(m);
}


int qs (int iterate, char* ptr)
{
    int sum = 0;
    char *p = ptr;
    while (*p) {
        if (*p < '0' || *p > '9') {
            exit(1);
        }
        sum += *p - '0';
        ++p;
    }
    return iterate? qsn(sum): sum;
}


int main (int argc, char** argv)
{
    int index = 1;
    if (argc < 2) {
        usage();
    }
    if (!strcmp(argv[1], "-i")) {
        if (argc < 3) {
            usage();
        }
        ++index;
    }
    printf ("%d\n", qs(index == 2, argv[index]));
}
