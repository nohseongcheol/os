#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *varg_VALUE) { size_t gjatësi_VALUE = 0; while (varg_VALUE[gjatësi_VALUE]) gjatësi_VALUE++; return gjatësi_VALUE; }
int strcmp(const char *e_përparme_VALUE, const char *PAS_VALUE) {
    while (*e_përparme_VALUE && *e_përparme_VALUE == *PAS_VALUE) { e_përparme_VALUE++; PAS_VALUE++; }
    return (unsigned char)*e_përparme_VALUE - (unsigned char)*PAS_VALUE;
}
int memcmp(const void *e_përparme_VALUE, const void *PAS_VALUE, size_t bajt_COUNT) {
    const unsigned char *가 = e_përparme_VALUE, *나 = PAS_VALUE;
    for (size_t hapësirë_për_tekst_futje = 0; hapësirë_për_tekst_futje < bajt_COUNT; hapësirë_për_tekst_futje++) if (가[hapësirë_për_tekst_futje] != 나[hapësirë_për_tekst_futje]) return 가[hapësirë_për_tekst_futje] - 나[hapësirë_për_tekst_futje];
    return 0;
}
void *memcpy(void *vendmbërritje_VALUE, const void *원본, size_t bajt_COUNT) {
    unsigned char *가 = vendmbërritje_VALUE; const unsigned char *나 = 원본;
    for (size_t hapësirë_për_tekst_futje = 0; hapësirë_për_tekst_futje < bajt_COUNT; hapësirë_për_tekst_futje++) 가[hapësirë_për_tekst_futje] = 나[hapësirë_për_tekst_futje];
    return vendmbërritje_VALUE;
}
void *memset(void *vendmbërritje_VALUE, int VALUE, size_t bajt_COUNT) {
    unsigned char *të_dhëna = vendmbërritje_VALUE;
    for (size_t hapësirë_për_tekst_futje = 0; hapësirë_për_tekst_futje < bajt_COUNT; hapësirë_për_tekst_futje++) të_dhëna[hapësirë_për_tekst_futje] = VALUE;
    return vendmbërritje_VALUE;
}
int putchar(int 문자) { unsigned char VALUE = 문자; return write(1, &VALUE, 1) == 1 ? VALUE : EOF; }
int puts(const char *varg_VALUE) {
    size_t gjatësi_VALUE = strlen(varg_VALUE), Pozicioni = 0;
    while (Pozicioni < gjatësi_VALUE) { ssize_t llogaritje = write(1, varg_VALUE + Pozicioni, gjatësi_VALUE - Pozicioni); if (llogaritje <= 0) return EOF; Pozicioni += llogaritje; }
    return putchar('\n') == EOF ? EOF : 0;
}
