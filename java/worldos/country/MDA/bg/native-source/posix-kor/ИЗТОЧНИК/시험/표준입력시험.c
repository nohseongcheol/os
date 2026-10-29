#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int 개수, char **запис_Списък) {
    (void)개수; (void)запис_Списък;
    char данни[6]; int 길이 = 0;
    puts("POSIX INPUT READY");
    while (길이 < 6) {
        int РЕЗУЛТАТ = 파일자료읽기(0, данни + 길이, 6 - 길이);
        if (РЕЗУЛТАТ <= 0) return 1;
        길이 += РЕЗУЛТАТ;
    }
    if (memcmp(данни, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
