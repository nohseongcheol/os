#include <파일규약.h>
#include <stdio.h>
int main(int Element_COUNT, char **Agab_Lëscht) {
    (void)Element_COUNT; (void)Agab_Lëscht;
    int Fichier = ariichten_Fichier("stored.txt", lies_schreiffäeg | 없으면만들기 | 내용비우기, 0600);
    if (Fichier < 0 || schreiwen_Fichier_Daten(Fichier, "saved-from-C", 12) != 12) return 1;
    if (파일저장확정(Fichier) < 0) return 2;
    if (Clôture_Fichier(Fichier) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}
