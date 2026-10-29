#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int vara_COUNT, char **færsla_Listi) {
    (void)vara_COUNT; (void)færsla_Listi;
    char gögn[6]; int lengd_VALUE = 0;
    puts("POSIX INPUT READY");
    while (lengd_VALUE < 6) {
        int NIÐURSTAÐA = 파일자료읽기(0, gögn + lengd_VALUE, 6 - lengd_VALUE);
        if (NIÐURSTAÐA <= 0) return 1;
        lengd_VALUE += NIÐURSTAÐA;
    }
    if (memcmp(gögn, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
