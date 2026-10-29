#include <파일규약.h>
#include <stdio.h>
int main(int vare_ANTALL, char **oppføring_Liste) {
    (void)vare_ANTALL; (void)oppføring_Liste;
    int Fil = åpen_Fil("stored.txt", lese_og_skrive | 없으면만들기 | avkorte_Innhold, 0600);
    if (Fil < 0 || skrive_Fil_data(Fil, "saved-from-C", 12) != 12) return 1;
    if (파일저장확정(Fil) < 0) return 2;
    if (Lukk_Fil(Fil) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}
