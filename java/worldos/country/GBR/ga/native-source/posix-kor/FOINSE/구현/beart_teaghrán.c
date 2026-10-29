#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *teaghrán_VALUE) { size_t fad_VALUE = 0; while (teaghrán_VALUE[fad_VALUE]) fad_VALUE++; return fad_VALUE; }
int strcmp(const char *앞, const char *Siar_VALUE) {
    while (*앞 && *앞 == *Siar_VALUE) { 앞++; Siar_VALUE++; }
    return (unsigned char)*앞 - (unsigned char)*Siar_VALUE;
}
int memcmp(const void *앞, const void *Siar_VALUE, size_t beart_COUNT) {
    const unsigned char *가 = 앞, *나 = Siar_VALUE;
    for (size_t spás_iontráil = 0; spás_iontráil < beart_COUNT; spás_iontráil++) if (가[spás_iontráil] != 나[spás_iontráil]) return 가[spás_iontráil] - 나[spás_iontráil];
    return 0;
}
void *memcpy(void *sprioc_VALUE, const void *원본, size_t beart_COUNT) {
    unsigned char *가 = sprioc_VALUE; const unsigned char *나 = 원본;
    for (size_t spás_iontráil = 0; spás_iontráil < beart_COUNT; spás_iontráil++) 가[spás_iontráil] = 나[spás_iontráil];
    return sprioc_VALUE;
}
void *memset(void *sprioc_VALUE, int VALUE, size_t beart_COUNT) {
    unsigned char *sonraí = sprioc_VALUE;
    for (size_t spás_iontráil = 0; spás_iontráil < beart_COUNT; spás_iontráil++) sonraí[spás_iontráil] = VALUE;
    return sprioc_VALUE;
}
int putchar(int 문자) { unsigned char VALUE = 문자; return write(1, &VALUE, 1) == 1 ? VALUE : EOF; }
int puts(const char *teaghrán_VALUE) {
    size_t fad_VALUE = strlen(teaghrán_VALUE), suíomh = 0;
    while (suíomh < fad_VALUE) { ssize_t tomhas = write(1, teaghrán_VALUE + suíomh, fad_VALUE - suíomh); if (tomhas <= 0) return EOF; suíomh += tomhas; }
    return putchar('\n') == EOF ? EOF : 0;
}
