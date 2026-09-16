/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <unistd.h>
int __posix_library_test(void);
int main(void)
{
    int test_line = __posix_library_test();
    if (test_line) {
        char buffer[16];
        int length = 0;
        অল(1, "POSIX-LIBRARY:FAIL line=", 24);
        do { buffer[length++] = (char)('0' + test_line % 10); test_line /= 10; } while (test_line);
        while (length) অল(1, &buffer[--length], 1);
        অল(1, "\n", 1);
        return 1;
    }
    return অল(1, "POSIX-LIBRARY:PASS\n", 19) == 19 ? 0 : 1;
}
