#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int 개수, char **увядзенне_Спіс) {
    (void)개수; (void)увядзенне_Спіс;
    char дадзеныя[6]; int даўжыня_значэнне = 0;
    puts("POSIX INPUT READY");
    while (даўжыня_значэнне < 6) {
        int 결과 = 파일자료읽기(0, дадзеныя + даўжыня_значэнне, 6 - даўжыня_значэнне);
        if (결과 <= 0) return 1;
        даўжыня_значэнне += 결과;
    }
    if (memcmp(дадзеныя, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
