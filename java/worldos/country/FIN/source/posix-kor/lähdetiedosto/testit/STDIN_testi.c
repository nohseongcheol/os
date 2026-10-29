#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int kohde_LASKE, char **merkintä_luettelo) {
    (void)kohde_LASKE; (void)merkintä_luettelo;
    char data[6]; int kesto_ARVO = 0;
    puts("POSIX INPUT READY");
    while (kesto_ARVO < 6) {
        int TULOS = lukea_Tiedosto_data(0, data + kesto_ARVO, 6 - kesto_ARVO);
        if (TULOS <= 0) return 1;
        kesto_ARVO += TULOS;
    }
    if (memcmp(data, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
