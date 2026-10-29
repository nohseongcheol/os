#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int 개수, char **girizmeklik_Sanaw) {
    (void)개수; (void)girizmeklik_Sanaw;
    char maglumat[6]; int dowamlylyk_baha = 0;
    puts("POSIX INPUT READY");
    while (dowamlylyk_baha < 6) {
        int 결과 = 파일자료읽기(0, maglumat + dowamlylyk_baha, 6 - dowamlylyk_baha);
        if (결과 <= 0) return 1;
        dowamlylyk_baha += 결과;
    }
    if (memcmp(maglumat, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
