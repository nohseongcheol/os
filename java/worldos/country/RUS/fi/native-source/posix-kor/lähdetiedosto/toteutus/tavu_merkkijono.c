#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *merkkijono_ARVO) { size_t kesto_ARVO = 0; while (merkkijono_ARVO[kesto_ARVO]) kesto_ARVO++; return kesto_ARVO; }
int strcmp(const char *etukamera_ARVO, const char *BACK_ARVO) {
    while (*etukamera_ARVO && *etukamera_ARVO == *BACK_ARVO) { etukamera_ARVO++; BACK_ARVO++; }
    return (unsigned char)*etukamera_ARVO - (unsigned char)*BACK_ARVO;
}
int memcmp(const void *etukamera_ARVO, const void *BACK_ARVO, size_t tavu_LASKE) {
    const unsigned char *가 = etukamera_ARVO, *SEKUNNIT_operandi = BACK_ARVO;
    for (size_t paikka_merkintä = 0; paikka_merkintä < tavu_LASKE; paikka_merkintä++) if (가[paikka_merkintä] != SEKUNNIT_operandi[paikka_merkintä]) return 가[paikka_merkintä] - SEKUNNIT_operandi[paikka_merkintä];
    return 0;
}
void *memcpy(void *kohde_ARVO, const void *원본, size_t tavu_LASKE) {
    unsigned char *가 = kohde_ARVO; const unsigned char *SEKUNNIT_operandi = 원본;
    for (size_t paikka_merkintä = 0; paikka_merkintä < tavu_LASKE; paikka_merkintä++) 가[paikka_merkintä] = SEKUNNIT_operandi[paikka_merkintä];
    return kohde_ARVO;
}
void *memset(void *kohde_ARVO, int ARVO, size_t tavu_LASKE) {
    unsigned char *data = kohde_ARVO;
    for (size_t paikka_merkintä = 0; paikka_merkintä < tavu_LASKE; paikka_merkintä++) data[paikka_merkintä] = ARVO;
    return kohde_ARVO;
}
int putchar(int 문자) { unsigned char ARVO = 문자; return write(1, &ARVO, 1) == 1 ? ARVO : EOF; }
int puts(const char *merkkijono_ARVO) {
    size_t kesto_ARVO = strlen(merkkijono_ARVO), paikka = 0;
    while (paikka < kesto_ARVO) { ssize_t TULOS = write(1, merkkijono_ARVO + paikka, kesto_ARVO - paikka); if (TULOS <= 0) return EOF; paikka += TULOS; }
    return putchar('\n') == EOF ? EOF : 0;
}
