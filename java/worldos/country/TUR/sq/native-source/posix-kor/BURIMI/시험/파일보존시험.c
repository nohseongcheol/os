#include <파일규약.h>
#include <stdio.h>
int main(int njësi_COUNT, char **futje_Listë) {
    (void)njësi_COUNT; (void)futje_Listë;
    int Kartelë = hap_skedar("stored.txt", lexoj_shkruaj | 없으면만들기 | 내용비우기, 0600);
    if (Kartelë < 0 || shkruaj_skedar_të_dhëna(Kartelë, "saved-from-C", 12) != 12) return 1;
    if (파일저장확정(Kartelë) < 0) return 2;
    if (mbyll_skedar(Kartelë) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}
