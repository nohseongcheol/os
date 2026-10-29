#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int 개수, char **اندراج_فہرست) {
    (void)개수; (void)اندراج_فہرست;
    char کوائف[6]; int لمبا_ئی_قدر = 0;
    puts("POSIX INPUT READY");
    while (لمبا_ئی_قدر < 6) {
        int پیمائش = 파일자료읽기(0, کوائف + لمبا_ئی_قدر, 6 - لمبا_ئی_قدر);
        if (پیمائش <= 0) return 1;
        لمبا_ئی_قدر += پیمائش;
    }
    if (memcmp(کوائف, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
