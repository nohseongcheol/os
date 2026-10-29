#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int nì_COUNT, char **cur_a_steach_Liosta) {
    (void)nì_COUNT; (void)cur_a_steach_Liosta;
    char dàta[6]; int faid_VALUE = 0;
    puts("POSIX INPUT READY");
    while (faid_VALUE < 6) {
        int tomhas = 파일자료읽기(0, dàta + faid_VALUE, 6 - faid_VALUE);
        if (tomhas <= 0) return 1;
        faid_VALUE += tomhas;
    }
    if (memcmp(dàta, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
