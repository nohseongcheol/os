/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <unistd.h>
int __posix_library_test(void);
int main(void)
{
    int test_line = __posix_library_test();
    if (test_line) {
        char منتقلی_کا_عارضی_ذخیرہ_2[16];
        int لمبائی = 0;
        لکھنا(1, "POSIX-LIBRARY:FAIL line=", 24);
        do { منتقلی_کا_عارضی_ذخیرہ_2[لمبائی++] = (char)('0' + test_line % 10); test_line /= 10; } while (test_line);
        while (لمبائی) لکھنا(1, &منتقلی_کا_عارضی_ذخیرہ_2[--لمبائی], 1);
        لکھنا(1, "\n", 1);
        return 1;
    }
    return لکھنا(1, "POSIX-LIBRARY:PASS\n", 19) == 19 ? 0 : 1;
}
