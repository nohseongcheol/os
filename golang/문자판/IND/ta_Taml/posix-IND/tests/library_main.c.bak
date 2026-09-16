#include <unistd.h>
int __posix_library_test(void);
int main(void)
{
    int test_line = __posix_library_test();
    if (test_line) {
        char பரிமாற்ற_இடையகம்_2[16];
        int நீளம் = 0;
        எழுது(1, "POSIX-LIBRARY:FAIL line=", 24);
        do { பரிமாற்ற_இடையகம்_2[நீளம்++] = (char)('0' + test_line % 10); test_line /= 10; } while (test_line);
        while (நீளம்) எழுது(1, &பரிமாற்ற_இடையகம்_2[--நீளம்], 1);
        எழுது(1, "\n", 1);
        return 1;
    }
    return எழுது(1, "POSIX-LIBRARY:PASS\n", 19) == 19 ? 0 : 1;
}
