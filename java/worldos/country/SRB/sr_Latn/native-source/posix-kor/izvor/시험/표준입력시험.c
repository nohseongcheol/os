#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int stavka_COUNT, char **stavka_Lista) {
    (void)stavka_COUNT; (void)stavka_Lista;
    char podaci[6]; int 길이 = 0;
    puts("POSIX INPUT READY");
    while (길이 < 6) {
        int KR = 파일자료읽기(0, podaci + 길이, 6 - 길이);
        if (KR <= 0) return 1;
        길이 += KR;
    }
    if (memcmp(podaci, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
