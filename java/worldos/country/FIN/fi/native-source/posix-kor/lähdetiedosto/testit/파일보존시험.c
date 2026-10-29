#include <파일규약.h>
#include <stdio.h>
int main(int kohde_LASKE, char **merkintä_luettelo) {
    (void)kohde_LASKE; (void)merkintä_luettelo;
    int tiedoston_nimi = avata_Tiedosto("stored.txt", luku_ja_kirjoitus | 없으면만들기 | 내용비우기, 0600);
    if (tiedoston_nimi < 0 || kirjoitus_Tiedosto_data(tiedoston_nimi, "saved-from-C", 12) != 12) return 1;
    if (vahvistaa_muutokset_Files(tiedoston_nimi) < 0) return 2;
    if (Sulje_Tiedosto(tiedoston_nimi) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}
