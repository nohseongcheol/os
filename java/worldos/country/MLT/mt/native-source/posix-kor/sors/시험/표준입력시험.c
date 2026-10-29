#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int element_COUNT, char **entrata_Lista) {
    (void)element_COUNT; (void)entrata_Lista;
    char data[6]; int tul_VALUE = 0;
    puts("POSIX INPUT READY");
    while (tul_VALUE < 6) {
        int miżura = 파일자료읽기(0, data + tul_VALUE, 6 - tul_VALUE);
        if (miżura <= 0) return 1;
        tul_VALUE += miżura;
    }
    if (memcmp(data, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
