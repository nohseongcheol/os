#include <파일규약.h>
#include <stdio.h>
int main(int element_COUNT, char **vnos_Seznam) {
    (void)element_COUNT; (void)vnos_Seznam;
    int Datoteka = odprto_Datoteka("stored.txt", branje_pisanje | 없으면만들기 | 내용비우기, 0600);
    if (Datoteka < 0 || pisati_Datoteka_podatki(Datoteka, "saved-from-C", 12) != 12) return 1;
    if (potrjevanje_datotečna_shramba(Datoteka) < 0) return 2;
    if (Zapri_Datoteka(Datoteka) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}
