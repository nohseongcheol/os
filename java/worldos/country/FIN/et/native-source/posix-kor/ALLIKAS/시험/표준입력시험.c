#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int kaup_COUNT, char **kirje_Loend) {
    (void)kaup_COUNT; (void)kirje_Loend;
    char andmed[6]; int 길이 = 0;
    puts("POSIX INPUT READY");
    while (길이 < 6) {
        int TULEMUS = 파일자료읽기(0, andmed + 길이, 6 - 길이);
        if (TULEMUS <= 0) return 1;
        길이 += TULEMUS;
    }
    if (memcmp(andmed, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
