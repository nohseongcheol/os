#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int 개수, char **унос_списак) {
    (void)개수; (void)унос_списак;
    char подаци[6]; int дужина_вриједност = 0;
    puts("POSIX INPUT READY");
    while (дужина_вриједност < 6) {
        int 결과 = 파일자료읽기(0, подаци + дужина_вриједност, 6 - дужина_вриједност);
        if (결과 <= 0) return 1;
        дужина_вриједност += 결과;
    }
    if (memcmp(подаци, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
