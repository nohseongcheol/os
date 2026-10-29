#include <파일규약.h>
#include <stdio.h>
int main(int 개수, char **ufako_nkcukacha_uludwe) {
    (void)개수; (void)ufako_nkcukacha_uludwe;
    int iFayili = vula_ifayile("stored.txt", funda_bhala | 없으면만들기 | 내용비우기, 0600);
    if (iFayili < 0 || bhala_ifayile_iingcombolo(iFayili, "saved-from-C", 12) != 12) return 1;
    if (파일저장확정(iFayili) < 0) return 2;
    if (vala_ifayile(iFayili) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}
