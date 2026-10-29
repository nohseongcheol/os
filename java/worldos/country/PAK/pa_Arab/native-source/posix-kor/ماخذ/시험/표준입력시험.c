#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int 개수, char **داخلہ_فرست) {
    (void)개수; (void)داخلہ_فرست;
    char کوائف[6]; int لمبائی_قدر = 0;
    puts("POSIX INPUT READY");
    while (لمبائی_قدر < 6) {
        int 결과 = 파일자료읽기(0, کوائف + لمبائی_قدر, 6 - لمبائی_قدر);
        if (결과 <= 0) return 1;
        لمبائی_قدر += 결과;
    }
    if (memcmp(کوائف, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
