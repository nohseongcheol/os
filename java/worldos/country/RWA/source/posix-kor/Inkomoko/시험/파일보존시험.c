#include <파일규약.h>
#include <stdio.h>
int main(int 개수, char **icyinjizwa_Urutonde) {
    (void)개수; (void)icyinjizwa_Urutonde;
    int Idosiye = kurema_dosiye("stored.txt", gusoma_kwandika | 없으면만들기 | 내용비우기, 0600);
    if (Idosiye < 0 || kwandika_dosiye_amakurushingiro(Idosiye, "saved-from-C", 12) != 12) return 1;
    if (파일저장확정(Idosiye) < 0) return 2;
    if (gufunga_dosiye(Idosiye) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}
