#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int tuemi_COUNT, char **tāurunga_Rārangi) {
    (void)tuemi_COUNT; (void)tāurunga_Rārangi;
    char raraunga[6]; int roa_uara = 0;
    puts("POSIX INPUT READY");
    while (roa_uara < 6) {
        int mēhua = 파일자료읽기(0, raraunga + roa_uara, 6 - roa_uara);
        if (mēhua <= 0) return 1;
        roa_uara += mēhua;
    }
    if (memcmp(raraunga, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
