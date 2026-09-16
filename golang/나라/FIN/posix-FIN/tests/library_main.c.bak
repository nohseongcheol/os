#include <unistd.h>
int __posix_library_test(void);
int main(void)
{
    int test_line = __posix_library_test();
    if (test_line) {
        char siirtopuskuri_2[16];
        int pituus = 0;
        Kirjoitus(1, "POSIX-LIBRARY:FAIL line=", 24);
        do { siirtopuskuri_2[pituus++] = (char)('0' + test_line % 10); test_line /= 10; } while (test_line);
        while (pituus) Kirjoitus(1, &siirtopuskuri_2[--pituus], 1);
        Kirjoitus(1, "\n", 1);
        return 1;
    }
    return Kirjoitus(1, "POSIX-LIBRARY:PASS\n", 19) == 19 ? 0 : 1;
}
