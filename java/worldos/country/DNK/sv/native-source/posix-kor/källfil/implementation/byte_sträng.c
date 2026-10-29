#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *sträng_värde) { size_t längd_värde = 0; while (sträng_värde[längd_värde]) längd_värde++; return längd_värde; }
int strcmp(const char *framåtvänd_värde, const char *BACK_värde) {
    while (*framåtvänd_värde && *framåtvänd_värde == *BACK_värde) { framåtvänd_värde++; BACK_värde++; }
    return (unsigned char)*framåtvänd_värde - (unsigned char)*BACK_värde;
}
int memcmp(const void *framåtvänd_värde, const void *BACK_värde, size_t byte_ANTAL) {
    const unsigned char *가 = framåtvänd_värde, *SEKUND_operand = BACK_värde;
    for (size_t fack_post = 0; fack_post < byte_ANTAL; fack_post++) if (가[fack_post] != SEKUND_operand[fack_post]) return 가[fack_post] - SEKUND_operand[fack_post];
    return 0;
}
void *memcpy(void *mål_värde, const void *원본, size_t byte_ANTAL) {
    unsigned char *가 = mål_värde; const unsigned char *SEKUND_operand = 원본;
    for (size_t fack_post = 0; fack_post < byte_ANTAL; fack_post++) 가[fack_post] = SEKUND_operand[fack_post];
    return mål_värde;
}
void *memset(void *mål_värde, int värde, size_t byte_ANTAL) {
    unsigned char *data = mål_värde;
    for (size_t fack_post = 0; fack_post < byte_ANTAL; fack_post++) data[fack_post] = värde;
    return mål_värde;
}
int putchar(int 문자) { unsigned char värde = 문자; return write(1, &värde, 1) == 1 ? värde : EOF; }
int puts(const char *sträng_värde) {
    size_t längd_värde = strlen(sträng_värde), position = 0;
    while (position < längd_värde) { ssize_t RESULTAT = write(1, sträng_värde + position, längd_värde - position); if (RESULTAT <= 0) return EOF; position += RESULTAT; }
    return putchar('\n') == EOF ? EOF : 0;
}
