#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int cikk_DARAB, char **bejegyzés_Lista) {
    (void)cikk_DARAB; (void)bejegyzés_Lista;
    char adat[6]; int hossz_ÉRTÉK = 0;
    puts("POSIX INPUT READY");
    while (hossz_ÉRTÉK < 6) {
        int KR = 파일자료읽기(0, adat + hossz_ÉRTÉK, 6 - hossz_ÉRTÉK);
        if (KR <= 0) return 1;
        hossz_ÉRTÉK += KR;
    }
    if (memcmp(adat, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
