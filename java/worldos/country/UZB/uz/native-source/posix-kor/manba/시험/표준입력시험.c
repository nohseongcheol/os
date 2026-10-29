#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int element_COUNT, char **kiritish_Ro_yxat) {
    (void)element_COUNT; (void)kiritish_Ro_yxat;
    char ma_lumotlar[6]; int uzunlik_VALUE = 0;
    puts("POSIX INPUT READY");
    while (uzunlik_VALUE < 6) {
        int o_lchov = 파일자료읽기(0, ma_lumotlar + uzunlik_VALUE, 6 - uzunlik_VALUE);
        if (o_lchov <= 0) return 1;
        uzunlik_VALUE += o_lchov;
    }
    if (memcmp(ma_lumotlar, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
