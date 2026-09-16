/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <unistd.h>
int __posix_library_test(void);
int main(void)
{
    int test_line = __posix_library_test();
    if (test_line) {
        char memoria_intermedia_de_transferencia_2[16];
        int longitud = 0;
        escribir(1, "POSIX-LIBRARY:FAIL line=", 24);
        do { memoria_intermedia_de_transferencia_2[longitud++] = (char)('0' + test_line % 10); test_line /= 10; } while (test_line);
        while (longitud) escribir(1, &memoria_intermedia_de_transferencia_2[--longitud], 1);
        escribir(1, "\n", 1);
        return 1;
    }
    return escribir(1, "POSIX-LIBRARY:PASS\n", 19) == 19 ? 0 : 1;
}
