#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int položka_COUNT, char **položka_Zoznam) {
    (void)položka_COUNT; (void)položka_Zoznam;
    char údaje[6]; int dĺžka_VALUE = 0;
    puts("POSIX INPUT READY");
    while (dĺžka_VALUE < 6) {
        int KR = 파일자료읽기(0, údaje + dĺžka_VALUE, 6 - dĺžka_VALUE);
        if (KR <= 0) return 1;
        dĺžka_VALUE += KR;
    }
    if (memcmp(údaje, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
