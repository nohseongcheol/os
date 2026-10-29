#include <파일규약.h>
#include <stdio.h>
int main(int 개수, char **ìgbéwọlé_Àtòkọ) {
    (void)개수; (void)ìgbéwọlé_Àtòkọ;
    int Fáìlì = ṣí_fáìlì("stored.txt", tí_a_lè_kà_tí_a_lè_kọ | 없으면만들기 | 내용비우기, 0600);
    if (Fáìlì < 0 || kọ_fáìlì_détà(Fáìlì, "saved-from-C", 12) != 12) return 1;
    if (파일저장확정(Fáìlì) < 0) return 2;
    if (pa_dé_fáìlì(Fáìlì) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}
