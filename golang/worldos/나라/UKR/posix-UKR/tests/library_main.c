#include <unistd.h>
int __posix_library_test(void);
int main(void)
{
    int test_line = __posix_library_test();
    if (test_line) {
        char буфер_передавання_2[16];
        int довжина = 0;
        Запис(1, "POSIX-LIBRARY:FAIL line=", 24);
        do { буфер_передавання_2[довжина++] = (char)('0' + test_line % 10); test_line /= 10; } while (test_line);
        while (довжина) Запис(1, &буфер_передавання_2[--довжина], 1);
        Запис(1, "\n", 1);
        return 1;
    }
    return Запис(1, "POSIX-LIBRARY:PASS\n", 19) == 19 ? 0 : 1;
}
