#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int item_COUNT, char **pagpasok_list) {
    (void)item_COUNT; (void)pagpasok_list;
    char data[6]; int haba_VALUE = 0;
    puts("POSIX INPUT READY");
    while (haba_VALUE < 6) {
        int sukat = 파일자료읽기(0, data + haba_VALUE, 6 - haba_VALUE);
        if (sukat <= 0) return 1;
        haba_VALUE += sukat;
    }
    if (memcmp(data, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
