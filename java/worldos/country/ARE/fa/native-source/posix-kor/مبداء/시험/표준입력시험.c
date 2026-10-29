#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int 개수, char **ورودی_لیست) {
    (void)개수; (void)ورودی_لیست;
    char داده_ها[6]; int طول_مقدار = 0;
    puts("POSIX INPUT READY");
    while (طول_مقدار < 6) {
        int سنجش = 파일자료읽기(0, داده_ها + طول_مقدار, 6 - طول_مقدار);
        if (سنجش <= 0) return 1;
        طول_مقدار += سنجش;
    }
    if (memcmp(داده_ها, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
