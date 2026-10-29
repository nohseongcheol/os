#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int 개수, char **목록) {
    (void)개수; (void)목록;
    char atijaaya[6]; int akaliaa_ajutuu = 0;
    puts("POSIX INPUT READY");
    while (akaliaa_ajutuu < 6) {
        int 결과 = 파일자료읽기(0, atijaaya + akaliaa_ajutuu, 6 - akaliaa_ajutuu);
        if (결과 <= 0) return 1;
        akaliaa_ajutuu += 결과;
    }
    if (memcmp(atijaaya, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
