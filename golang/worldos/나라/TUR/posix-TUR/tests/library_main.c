#include <unistd.h>
int __posix_library_test(void);
int main(void)
{
    int test_line = __posix_library_test();
    if (test_line) {
        char aktarım_ara_belleği_2[16];
        int uzunluk = 0;
        Yazma(1, "POSIX-LIBRARY:FAIL line=", 24);
        do { aktarım_ara_belleği_2[uzunluk++] = (char)('0' + test_line % 10); test_line /= 10; } while (test_line);
        while (uzunluk) Yazma(1, &aktarım_ara_belleği_2[--uzunluk], 1);
        Yazma(1, "\n", 1);
        return 1;
    }
    return Yazma(1, "POSIX-LIBRARY:PASS\n", 19) == 19 ? 0 : 1;
}
