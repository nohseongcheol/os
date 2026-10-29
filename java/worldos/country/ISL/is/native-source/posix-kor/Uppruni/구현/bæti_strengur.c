#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *strengur_VALUE) { size_t lengd_VALUE = 0; while (strengur_VALUE[lengd_VALUE]) lengd_VALUE++; return lengd_VALUE; }
int strcmp(const char *myndavél_að_framan_VALUE, const char *TIL_BAKA_VALUE) {
    while (*myndavél_að_framan_VALUE && *myndavél_að_framan_VALUE == *TIL_BAKA_VALUE) { myndavél_að_framan_VALUE++; TIL_BAKA_VALUE++; }
    return (unsigned char)*myndavél_að_framan_VALUE - (unsigned char)*TIL_BAKA_VALUE;
}
int memcmp(const void *myndavél_að_framan_VALUE, const void *TIL_BAKA_VALUE, size_t bæti_COUNT) {
    const unsigned char *가 = myndavél_að_framan_VALUE, *나 = TIL_BAKA_VALUE;
    for (size_t rauf_færsla = 0; rauf_færsla < bæti_COUNT; rauf_færsla++) if (가[rauf_færsla] != 나[rauf_færsla]) return 가[rauf_færsla] - 나[rauf_færsla];
    return 0;
}
void *memcpy(void *endastaður_VALUE, const void *원본, size_t bæti_COUNT) {
    unsigned char *가 = endastaður_VALUE; const unsigned char *나 = 원본;
    for (size_t rauf_færsla = 0; rauf_færsla < bæti_COUNT; rauf_færsla++) 가[rauf_færsla] = 나[rauf_færsla];
    return endastaður_VALUE;
}
void *memset(void *endastaður_VALUE, int VALUE, size_t bæti_COUNT) {
    unsigned char *gögn = endastaður_VALUE;
    for (size_t rauf_færsla = 0; rauf_færsla < bæti_COUNT; rauf_færsla++) gögn[rauf_færsla] = VALUE;
    return endastaður_VALUE;
}
int putchar(int 문자) { unsigned char VALUE = 문자; return write(1, &VALUE, 1) == 1 ? VALUE : EOF; }
int puts(const char *strengur_VALUE) {
    size_t lengd_VALUE = strlen(strengur_VALUE), Staðsetning = 0;
    while (Staðsetning < lengd_VALUE) { ssize_t NIÐURSTAÐA = write(1, strengur_VALUE + Staðsetning, lengd_VALUE - Staðsetning); if (NIÐURSTAÐA <= 0) return EOF; Staðsetning += NIÐURSTAÐA; }
    return putchar('\n') == EOF ? EOF : 0;
}
