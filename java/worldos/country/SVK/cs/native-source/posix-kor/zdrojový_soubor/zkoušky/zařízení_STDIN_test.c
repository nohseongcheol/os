#include <Soubor_ABI.h>
#include <stdio.h>
#include <string.h>
int main(int zboží_POČET, char **položka_Seznam) {
    (void)zboží_POČET; (void)položka_Seznam;
    char data[6]; int délka_HODNOTA = 0;
    puts("POSIX INPUT READY");
    while (délka_HODNOTA < 6) {
        int VÝSLEDEK = 파일자료읽기(0, data + délka_HODNOTA, 6 - délka_HODNOTA);
        if (VÝSLEDEK <= 0) return 1;
        délka_HODNOTA += VÝSLEDEK;
    }
    if (memcmp(data, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
