#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int 개수, char **प्रविष्टि_सूची) {
    (void)개수; (void)प्रविष्टि_सूची;
    char लगत[6]; int लम्बाइ_मान = 0;
    puts("POSIX INPUT READY");
    while (लम्बाइ_मान < 6) {
        int मापन = 파일자료읽기(0, लगत + लम्बाइ_मान, 6 - लम्बाइ_मान);
        if (मापन <= 0) return 1;
        लम्बाइ_मान += मापन;
    }
    if (memcmp(लगत, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
