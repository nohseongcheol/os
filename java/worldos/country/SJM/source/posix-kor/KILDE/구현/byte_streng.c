#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *streng_VERDI) { size_t lengde_VERDI = 0; while (streng_VERDI[lengde_VERDI]) lengde_VERDI++; return lengde_VERDI; }
int strcmp(const char *frontkamera_VERDI, const char *TILBAKE_VERDI) {
    while (*frontkamera_VERDI && *frontkamera_VERDI == *TILBAKE_VERDI) { frontkamera_VERDI++; TILBAKE_VERDI++; }
    return (unsigned char)*frontkamera_VERDI - (unsigned char)*TILBAKE_VERDI;
}
int memcmp(const void *frontkamera_VERDI, const void *TILBAKE_VERDI, size_t byte_ANTALL) {
    const unsigned char *가 = frontkamera_VERDI, *SEKUND_operand = TILBAKE_VERDI;
    for (size_t åpning_oppføring = 0; åpning_oppføring < byte_ANTALL; åpning_oppføring++) if (가[åpning_oppføring] != SEKUND_operand[åpning_oppføring]) return 가[åpning_oppføring] - SEKUND_operand[åpning_oppføring];
    return 0;
}
void *memcpy(void *mål_VERDI, const void *원본, size_t byte_ANTALL) {
    unsigned char *가 = mål_VERDI; const unsigned char *SEKUND_operand = 원본;
    for (size_t åpning_oppføring = 0; åpning_oppføring < byte_ANTALL; åpning_oppføring++) 가[åpning_oppføring] = SEKUND_operand[åpning_oppføring];
    return mål_VERDI;
}
void *memset(void *mål_VERDI, int VERDI, size_t byte_ANTALL) {
    unsigned char *data = mål_VERDI;
    for (size_t åpning_oppføring = 0; åpning_oppføring < byte_ANTALL; åpning_oppføring++) data[åpning_oppføring] = VERDI;
    return mål_VERDI;
}
int putchar(int 문자) { unsigned char VERDI = 문자; return write(1, &VERDI, 1) == 1 ? VERDI : EOF; }
int puts(const char *streng_VERDI) {
    size_t lengde_VERDI = strlen(streng_VERDI), Posisjon = 0;
    while (Posisjon < lengde_VERDI) { ssize_t KR = write(1, streng_VERDI + Posisjon, lengde_VERDI - Posisjon); if (KR <= 0) return EOF; Posisjon += KR; }
    return putchar('\n') == EOF ? EOF : 0;
}
