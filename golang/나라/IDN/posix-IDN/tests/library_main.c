/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <unistd.h>
int __posix_library_test(void);
int main(void)
{
    int test_line = __posix_library_test();
    if (test_line) {
        char penyangga_transfer_2[16];
        int panjang = 0;
        Tulis(1, "POSIX-LIBRARY:FAIL line=", 24);
        do { penyangga_transfer_2[panjang++] = (char)('0' + test_line % 10); test_line /= 10; } while (test_line);
        while (panjang) Tulis(1, &penyangga_transfer_2[--panjang], 1);
        Tulis(1, "\n", 1);
        return 1;
    }
    return Tulis(1, "POSIX-LIBRARY:PASS\n", 19) == 19 ? 0 : 1;
}
