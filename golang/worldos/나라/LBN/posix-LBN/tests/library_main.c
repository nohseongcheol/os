#include <unistd.h>
int __posix_library_test(void);
int main(void)
{
    int test_line = __posix_library_test();
    if (test_line) {
        char مخزن_النقل_المؤقت_2[16];
        int الطول = 0;
        كتابة(1, "POSIX-LIBRARY:FAIL line=", 24);
        do { مخزن_النقل_المؤقت_2[الطول++] = (char)('0' + test_line % 10); test_line /= 10; } while (test_line);
        while (الطول) كتابة(1, &مخزن_النقل_المؤقت_2[--الطول], 1);
        كتابة(1, "\n", 1);
        return 1;
    }
    return كتابة(1, "POSIX-LIBRARY:PASS\n", 19) == 19 ? 0 : 1;
}
