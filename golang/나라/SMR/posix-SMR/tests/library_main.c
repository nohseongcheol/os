/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <unistd.h>
int __posix_library_test(void);
int main(void)
{
    int test_line = __posix_library_test();
    if (test_line) {
        char memoria_intermedia_di_trasferimento_2[16];
        int lunghezza = 0;
        Scrittura(1, "POSIX-LIBRARY:FAIL line=", 24);
        do { memoria_intermedia_di_trasferimento_2[lunghezza++] = (char)('0' + test_line % 10); test_line /= 10; } while (test_line);
        while (lunghezza) Scrittura(1, &memoria_intermedia_di_trasferimento_2[--lunghezza], 1);
        Scrittura(1, "\n", 1);
        return 1;
    }
    return Scrittura(1, "POSIX-LIBRARY:PASS\n", 19) == 19 ? 0 : 1;
}
