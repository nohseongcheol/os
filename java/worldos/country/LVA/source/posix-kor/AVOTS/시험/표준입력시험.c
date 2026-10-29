#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int krājums_COUNT, char **ievade_Saraksts) {
    (void)krājums_COUNT; (void)ievade_Saraksts;
    char dati[6]; int 길이 = 0;
    puts("POSIX INPUT READY");
    while (길이 < 6) {
        int mērs = 파일자료읽기(0, dati + 길이, 6 - 길이);
        if (mērs <= 0) return 1;
        길이 += mērs;
    }
    if (memcmp(dati, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
