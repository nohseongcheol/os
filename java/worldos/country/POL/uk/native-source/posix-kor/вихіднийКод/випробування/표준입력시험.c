#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int 개수, char **запис_список) {
    (void)개수; (void)запис_список;
    char дані[6]; int 길이 = 0;
    puts("POSIX INPUT READY");
    while (길이 < 6) {
        int результат = 파일자료읽기(0, дані + 길이, 6 - 길이);
        if (результат <= 0) return 1;
        길이 += результат;
    }
    if (memcmp(дані, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
