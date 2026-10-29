#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int vare_ANTALL, char **oppføring_Liste) {
    (void)vare_ANTALL; (void)oppføring_Liste;
    char data[6]; int lengde_VERDI = 0;
    puts("POSIX INPUT READY");
    while (lengde_VERDI < 6) {
        int KR = 파일자료읽기(0, data + lengde_VERDI, 6 - lengde_VERDI);
        if (KR <= 0) return 1;
        lengde_VERDI += KR;
    }
    if (memcmp(data, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
