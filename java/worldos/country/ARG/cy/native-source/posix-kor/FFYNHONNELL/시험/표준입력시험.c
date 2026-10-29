#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int eitem_COUNT, char **cofnod_Rhestr) {
    (void)eitem_COUNT; (void)cofnod_Rhestr;
    char data[6]; int hyd_VALUE = 0;
    puts("POSIX INPUT READY");
    while (hyd_VALUE < 6) {
        int mesur = 파일자료읽기(0, data + hyd_VALUE, 6 - hyd_VALUE);
        if (mesur <= 0) return 1;
        hyd_VALUE += mesur;
    }
    if (memcmp(data, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
