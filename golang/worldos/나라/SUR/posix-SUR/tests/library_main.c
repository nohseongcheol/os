#include <unistd.h>
int __posix_library_test(void);
int main(void)
{
    int test_line = __posix_library_test();
    if (test_line) {
        char overdrachtsbuffer_2[16];
        int lengte = 0;
        Schrijven(1, "POSIX-LIBRARY:FAIL line=", 24);
        do { overdrachtsbuffer_2[lengte++] = (char)('0' + test_line % 10); test_line /= 10; } while (test_line);
        while (lengte) Schrijven(1, &overdrachtsbuffer_2[--lengte], 1);
        Schrijven(1, "\n", 1);
        return 1;
    }
    return Schrijven(1, "POSIX-LIBRARY:PASS\n", 19) == 19 ? 0 : 1;
}
