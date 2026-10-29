#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int 개수, char **dugal_xabaar_lim) {
    (void)개수; (void)dugal_xabaar_lim;
    char mbir[6]; int diir_xëyma = 0;
    puts("POSIX INPUT READY");
    while (diir_xëyma < 6) {
        int 결과 = 파일자료읽기(0, mbir + diir_xëyma, 6 - diir_xëyma);
        if (결과 <= 0) return 1;
        diir_xëyma += 결과;
    }
    if (memcmp(mbir, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
