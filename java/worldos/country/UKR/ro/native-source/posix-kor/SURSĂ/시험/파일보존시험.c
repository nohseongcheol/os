#include <파일규약.h>
#include <stdio.h>
int main(int element_COUNT, char **intrare_Listă) {
    (void)element_COUNT; (void)intrare_Listă;
    int Fișier = crea_Fișier("stored.txt", citire_scriere | 없으면만들기 | trunchia_TOC, 0600);
    if (Fișier < 0 || scriere_Fișier_date(Fișier, "saved-from-C", 12) != 12) return 1;
    if (comitere_Fișiere(Fișier) < 0) return 2;
    if (închide_Fișier(Fișier) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}
