#include <파일규약.h>
#include <stdio.h>
int main(int položka_COUNT, char **položka_Zoznam) {
    (void)položka_COUNT; (void)položka_Zoznam;
    int Súbor = otvoriť_Súbor("stored.txt", na_čítanie_a_zapisovanie | 없으면만들기 | skrátiť_Obsah, 0600);
    if (Súbor < 0 || zapísať_Súbor_údaje(Súbor, "saved-from-C", 12) != 12) return 1;
    if (potvrdenie_ukladací_priestor_súborov(Súbor) < 0) return 2;
    if (Zavrieť_Súbor(Súbor) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}
