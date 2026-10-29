#include <unistd.h>
int __posix_library_test(void);
int main(void)
{
    int test_line = __posix_library_test();
    if (test_line) {
        char buffer[16];
        int length = 0;
        skriva(1, "POSIX-LIBRARY:FAIL line=", 24);
        do { buffer[length++] = (char)('0' + test_line % 10); test_line /= 10; } while (test_line);
        while (length) skriva(1, &buffer[--length], 1);
        skriva(1, "\n", 1);
        return 1;
    }
    return skriva(1, "POSIX-LIBRARY:PASS\n", 19) == 19 ? 0 : 1;
}
