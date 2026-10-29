#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int 개수, char **унос_Листа) {
    (void)개수; (void)унос_Листа;
    char подаци[6]; int дужина_вриједност = 0;
    puts("POSIX INPUT READY");
    while (дужина_вриједност < 6) {
        int ИСХОД = 파일자료읽기(0, подаци + дужина_вриједност, 6 - дужина_вриједност);
        if (ИСХОД <= 0) return 1;
        дужина_вриједност += ИСХОД;
    }
    if (memcmp(подаци, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
