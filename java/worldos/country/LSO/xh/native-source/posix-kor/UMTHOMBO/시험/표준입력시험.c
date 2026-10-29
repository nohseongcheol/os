#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int 개수, char **ufako_nkcukacha_uludwe) {
    (void)개수; (void)ufako_nkcukacha_uludwe;
    char iingcombolo[6]; int ubude_ixabiso = 0;
    puts("POSIX INPUT READY");
    while (ubude_ixabiso < 6) {
        int 결과 = 파일자료읽기(0, iingcombolo + ubude_ixabiso, 6 - ubude_ixabiso);
        if (결과 <= 0) return 1;
        ubude_ixabiso += 결과;
    }
    if (memcmp(iingcombolo, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
