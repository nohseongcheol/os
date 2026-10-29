#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int stavka_COUNT, char **unos_spisak) {
    (void)stavka_COUNT; (void)unos_spisak;
    char podaci[6]; int dužina_VALUE = 0;
    puts("POSIX INPUT READY");
    while (dužina_VALUE < 6) {
        int mjera = 파일자료읽기(0, podaci + dužina_VALUE, 6 - dužina_VALUE);
        if (mjera <= 0) return 1;
        dužina_VALUE += mjera;
    }
    if (memcmp(podaci, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
