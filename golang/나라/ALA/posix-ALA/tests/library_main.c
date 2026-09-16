/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <unistd.h>
int __posix_library_test(void);
int main(void)
{
    int test_line = __posix_library_test();
    if (test_line) {
        char överföringsbuffert_2[16];
        int längd = 0;
        Skriv(1, "POSIX-LIBRARY:FAIL line=", 24);
        do { överföringsbuffert_2[längd++] = (char)('0' + test_line % 10); test_line /= 10; } while (test_line);
        while (längd) Skriv(1, &överföringsbuffert_2[--längd], 1);
        Skriv(1, "\n", 1);
        return 1;
    }
    return Skriv(1, "POSIX-LIBRARY:PASS\n", 19) == 19 ? 0 : 1;
}
