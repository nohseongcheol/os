#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int 개수, char **ingizo_Orodha) {
    (void)개수; (void)ingizo_Orodha;
    char data[6]; int urefu_thamani = 0;
    puts("POSIX INPUT READY");
    while (urefu_thamani < 6) {
        int 결과 = 파일자료읽기(0, data + urefu_thamani, 6 - urefu_thamani);
        if (결과 <= 0) return 1;
        urefu_thamani += 결과;
    }
    if (memcmp(data, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
