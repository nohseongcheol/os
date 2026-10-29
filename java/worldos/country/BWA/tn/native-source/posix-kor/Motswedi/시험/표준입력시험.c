#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int 개수, char **tsenyo_lenaane) {
    (void)개수; (void)tsenyo_lenaane;
    char tshedimosetso[6]; int boleele_Boleng = 0;
    puts("POSIX INPUT READY");
    while (boleele_Boleng < 6) {
        int 결과 = 파일자료읽기(0, tshedimosetso + boleele_Boleng, 6 - boleele_Boleng);
        if (결과 <= 0) return 1;
        boleele_Boleng += 결과;
    }
    if (memcmp(tshedimosetso, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
