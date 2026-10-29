#include <Soubor_ABI.h>
#include <stdio.h>
int main(int zboží_POČET, char **položka_Seznam) {
    (void)zboží_POČET; (void)položka_Seznam;
    int název_souboru = otevřít_Soubor("stored.txt", pro_čtení_i_zápis | 없으면만들기 | stříhat_Obsah, 0600);
    if (název_souboru < 0 || zápis_Soubor_data(název_souboru, "saved-from-C", 12) != 12) return 1;
    if (zápis_Files(název_souboru) < 0) return 2;
    if (Zavřít_Soubor(název_souboru) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}
