#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int vare_COUNT, char **oppføring_Liste) {
    (void)vare_COUNT; (void)oppføring_Liste;
    char data[6]; int lengd_VALUE = 0;
    puts("POSIX INPUT READY");
    while (lengd_VALUE < 6) {
        int forretningsmål = 파일자료읽기(0, data + lengd_VALUE, 6 - lengd_VALUE);
        if (forretningsmål <= 0) return 1;
        lengd_VALUE += forretningsmål;
    }
    if (memcmp(data, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
