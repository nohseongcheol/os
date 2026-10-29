#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int vare_TÆL, char **post_Liste) {
    (void)vare_TÆL; (void)post_Liste;
    char data[6]; int varighed_VÆRDI = 0;
    puts("POSIX INPUT READY");
    while (varighed_VÆRDI < 6) {
        int KR = 파일자료읽기(0, data + varighed_VÆRDI, 6 - varighed_VÆRDI);
        if (KR <= 0) return 1;
        varighed_VÆRDI += KR;
    }
    if (memcmp(data, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
