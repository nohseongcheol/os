#include <파일규약.h>
#include <stdio.h>
int main(int vare_COUNT, char **oppføring_Liste) {
    (void)vare_COUNT; (void)oppføring_Liste;
    int Fil = opne_fil("stored.txt", lese_og_skrivetilgang | 없으면만들기 | 내용비우기, 0600);
    if (Fil < 0 || skrive_fil_data(Fil, "saved-from-C", 12) != 12) return 1;
    if (파일저장확정(Fil) < 0) return 2;
    if (Lukk_fil(Fil) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}
