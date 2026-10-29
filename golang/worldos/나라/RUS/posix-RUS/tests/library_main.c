#include <unistd.h>
int __posix_library_test(void);
int main(void)
{
    int test_line = __posix_library_test();
    if (test_line) {
        char буфер_передачи_2[16];
        int длина = 0;
        писать(1, "POSIX-LIBRARY:FAIL line=", 24);
        do { буфер_передачи_2[длина++] = (char)('0' + test_line % 10); test_line /= 10; } while (test_line);
        while (длина) писать(1, &буфер_передачи_2[--длина], 1);
        писать(1, "\n", 1);
        return 1;
    }
    return писать(1, "POSIX-LIBRARY:PASS\n", 19) == 19 ? 0 : 1;
}
