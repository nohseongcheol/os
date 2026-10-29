#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int artikl_COUNT, char **unos_Popis) {
    (void)artikl_COUNT; (void)unos_Popis;
    char podaci[6]; int 길이 = 0;
    puts("POSIX INPUT READY");
    while (길이 < 6) {
        int REZULTAT = 파일자료읽기(0, podaci + 길이, 6 - 길이);
        if (REZULTAT <= 0) return 1;
        길이 += REZULTAT;
    }
    if (memcmp(podaci, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
