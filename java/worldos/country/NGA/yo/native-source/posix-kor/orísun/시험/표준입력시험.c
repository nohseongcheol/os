#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int 개수, char **ìgbéwọlé_Àtòkọ) {
    (void)개수; (void)ìgbéwọlé_Àtòkọ;
    char détà[6]; int gígùn_iye = 0;
    puts("POSIX INPUT READY");
    while (gígùn_iye < 6) {
        int 결과 = 파일자료읽기(0, détà + gígùn_iye, 6 - gígùn_iye);
        if (결과 <= 0) return 1;
        gígùn_iye += 결과;
    }
    if (memcmp(détà, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
