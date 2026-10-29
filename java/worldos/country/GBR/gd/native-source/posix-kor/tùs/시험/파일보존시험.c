#include <파일규약.h>
#include <stdio.h>
int main(int nì_COUNT, char **cur_a_steach_Liosta) {
    (void)nì_COUNT; (void)cur_a_steach_Liosta;
    int faidhle = fosgail_faidhle("stored.txt", so_leughte_so_sgrìobhte | 없으면만들기 | 내용비우기, 0600);
    if (faidhle < 0 || sgrìobh_faidhle_dàta(faidhle, "saved-from-C", 12) != 12) return 1;
    if (파일저장확정(faidhle) < 0) return 2;
    if (dùin_faidhle(faidhle) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}
