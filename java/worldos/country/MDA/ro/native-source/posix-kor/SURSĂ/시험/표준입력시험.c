#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int element_COUNT, char **intrare_Listă) {
    (void)element_COUNT; (void)intrare_Listă;
    char date[6]; int lungime_VALUE = 0;
    puts("POSIX INPUT READY");
    while (lungime_VALUE < 6) {
        int KR = 파일자료읽기(0, date + lungime_VALUE, 6 - lungime_VALUE);
        if (KR <= 0) return 1;
        lungime_VALUE += KR;
    }
    if (memcmp(date, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
