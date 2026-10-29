#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int 개수, char **داخلا_فهرست) {
    (void)개수; (void)داخلا_فهرست;
    char ڪوائف[6]; int لمبائي_قدر = 0;
    puts("POSIX INPUT READY");
    while (لمبائي_قدر < 6) {
        int 결과 = 파일자료읽기(0, ڪوائف + لمبائي_قدر, 6 - لمبائي_قدر);
        if (결과 <= 0) return 1;
        لمبائي_قدر += 결과;
    }
    if (memcmp(ڪوائف, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
