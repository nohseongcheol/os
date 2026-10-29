#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int 개수, char **목록) {
    (void)개수; (void)목록;
    char 자료[6]; int 길이 = 0;
    puts("POSIX INPUT READY");
    while (길이 < 6) {
        int 결과 = 파일자료읽기(0, 자료 + 길이, 6 - 길이);
        if (결과 <= 0) return 1;
        길이 += 결과;
    }
    if (memcmp(자료, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
