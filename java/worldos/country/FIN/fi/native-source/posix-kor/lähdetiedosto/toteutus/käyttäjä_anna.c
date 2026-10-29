#include "KUTSU_rajattu_alue.h"
extern int main(int 인수개수, char **argumentti_luettelo);
static char argumentti_Muisti[2048];
static char *argumentti_luettelo[18];
int jkoros_main(void) {
    int kohde_LASKE = jkoros_syscall(2, 0, 0, 0, 0, 0);
    if (kohde_LASKE < 0 || kohde_LASKE > 16) return 126;
    /* nykyinen_kohde 커널의 argv는 Suorita_komento 이름을 제외한다. C argv[0]은 고정 식별 이름이다. */
    argumentti_luettelo[0] = "jkoros-app";
    int paikka = 0;
    for (int INDEKSI = 0; INDEKSI < kohde_LASKE; INDEKSI++) {
        const int *원본 = (const int *)jkoros_syscall(3, INDEKSI, 0, 0, 0, 0);
        if (!원본 || 원본[0] < 0 || 원본[0] > 127) return 126;
        argumentti_luettelo[INDEKSI + 1] = argumentti_Muisti + paikka;
        for (int paikka_merkintä = 0; paikka_merkintä < 원본[0]; paikka_merkintä++) {
            if (paikka >= 2047) return 126;
            argumentti_Muisti[paikka++] = 원본[paikka_merkintä + 1];
        }
        argumentti_Muisti[paikka++] = 0;
    }
    argumentti_luettelo[kohde_LASKE + 1] = 0;
    return main(kohde_LASKE + 1, argumentti_luettelo);
}
