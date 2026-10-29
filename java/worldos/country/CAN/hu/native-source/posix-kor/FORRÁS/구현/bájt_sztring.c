#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *sztring_ÉRTÉK) { size_t hossz_ÉRTÉK = 0; while (sztring_ÉRTÉK[hossz_ÉRTÉK]) hossz_ÉRTÉK++; return hossz_ÉRTÉK; }
int strcmp(const char *elülső_kamera_ÉRTÉK, const char *BACK_ÉRTÉK) {
    while (*elülső_kamera_ÉRTÉK && *elülső_kamera_ÉRTÉK == *BACK_ÉRTÉK) { elülső_kamera_ÉRTÉK++; BACK_ÉRTÉK++; }
    return (unsigned char)*elülső_kamera_ÉRTÉK - (unsigned char)*BACK_ÉRTÉK;
}
int memcmp(const void *elülső_kamera_ÉRTÉK, const void *BACK_ÉRTÉK, size_t bájt_DARAB) {
    const unsigned char *가 = elülső_kamera_ÉRTÉK, *MPERC_operandus = BACK_ÉRTÉK;
    for (size_t tárolóhely_bejegyzés = 0; tárolóhely_bejegyzés < bájt_DARAB; tárolóhely_bejegyzés++) if (가[tárolóhely_bejegyzés] != MPERC_operandus[tárolóhely_bejegyzés]) return 가[tárolóhely_bejegyzés] - MPERC_operandus[tárolóhely_bejegyzés];
    return 0;
}
void *memcpy(void *cél_ÉRTÉK, const void *원본, size_t bájt_DARAB) {
    unsigned char *가 = cél_ÉRTÉK; const unsigned char *MPERC_operandus = 원본;
    for (size_t tárolóhely_bejegyzés = 0; tárolóhely_bejegyzés < bájt_DARAB; tárolóhely_bejegyzés++) 가[tárolóhely_bejegyzés] = MPERC_operandus[tárolóhely_bejegyzés];
    return cél_ÉRTÉK;
}
void *memset(void *cél_ÉRTÉK, int ÉRTÉK, size_t bájt_DARAB) {
    unsigned char *adat = cél_ÉRTÉK;
    for (size_t tárolóhely_bejegyzés = 0; tárolóhely_bejegyzés < bájt_DARAB; tárolóhely_bejegyzés++) adat[tárolóhely_bejegyzés] = ÉRTÉK;
    return cél_ÉRTÉK;
}
int putchar(int 문자) { unsigned char ÉRTÉK = 문자; return write(1, &ÉRTÉK, 1) == 1 ? ÉRTÉK : EOF; }
int puts(const char *sztring_ÉRTÉK) {
    size_t hossz_ÉRTÉK = strlen(sztring_ÉRTÉK), Pozíció = 0;
    while (Pozíció < hossz_ÉRTÉK) { ssize_t KR = write(1, sztring_ÉRTÉK + Pozíció, hossz_ÉRTÉK - Pozíció); if (KR <= 0) return EOF; Pozíció += KR; }
    return putchar('\n') == EOF ? EOF : 0;
}
