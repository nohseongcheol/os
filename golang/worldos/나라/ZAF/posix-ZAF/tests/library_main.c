#include <unistd.h>
int __posix_library_test(void);
int main(void)
{
    int test_line = __posix_library_test();
    if (test_line) {
        char transfer_buffer_2[16];
        int length = 0;
        write(1, "POSIX-LIBRARY:FAIL line=", 24);
        do { transfer_buffer_2[length++] = (char)('0' + test_line % 10); test_line /= 10; } while (test_line);
        while (length) write(1, &transfer_buffer_2[--length], 1);
        write(1, "\n", 1);
        return 1;
    }
    return write(1, "POSIX-LIBRARY:PASS\n", 19) == 19 ? 0 : 1;
}
