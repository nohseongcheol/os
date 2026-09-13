#include <unistd.h>
int __posix_library_test(void);
int main(void)
{
    int test_line = __posix_library_test();
    if (test_line) {
        char Übertragungspuffer_2[16];
        int Länge = 0;
        schreiben(1, "POSIX-LIBRARY:FAIL line=", 24);
        do { Übertragungspuffer_2[Länge++] = (char)('0' + test_line % 10); test_line /= 10; } while (test_line);
        while (Länge) schreiben(1, &Übertragungspuffer_2[--Länge], 1);
        schreiben(1, "\n", 1);
        return 1;
    }
    return schreiben(1, "POSIX-LIBRARY:PASS\n", 19) == 19 ? 0 : 1;
}
