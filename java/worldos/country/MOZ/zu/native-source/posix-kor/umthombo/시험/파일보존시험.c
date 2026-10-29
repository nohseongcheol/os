#include <파일규약.h>
#include <stdio.h>
int main(int 개수, char **okufakwayo_Uhlu) {
    (void)개수; (void)okufakwayo_Uhlu;
    int Ihele = vula_ifayela("stored.txt", fundeka_bhaleka | 없으면만들기 | 내용비우기, 0600);
    if (Ihele < 0 || bhala_ifayela_imininingwane(Ihele, "saved-from-C", 12) != 12) return 1;
    if (파일저장확정(Ihele) < 0) return 2;
    if (vala_ifayela(Ihele) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}
