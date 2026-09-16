#include <unistd.h>
int __posix_library_test(void);
int main(void)
{
    int test_line = __posix_library_test();
    if (test_line) {
        char bufor_przesyłania_2[16];
        int długość = 0;
        Zapis(1, "POSIX-LIBRARY:FAIL line=", 24);
        do { bufor_przesyłania_2[długość++] = (char)('0' + test_line % 10); test_line /= 10; } while (test_line);
        while (długość) Zapis(1, &bufor_przesyłania_2[--długość], 1);
        Zapis(1, "\n", 1);
        return 1;
    }
    return Zapis(1, "POSIX-LIBRARY:PASS\n", 19) == 19 ? 0 : 1;
}
