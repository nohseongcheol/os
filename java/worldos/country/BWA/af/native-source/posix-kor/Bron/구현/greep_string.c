#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *string_VALUE) { size_t lengte_VALUE = 0; while (string_VALUE[lengte_VALUE]) lengte_VALUE++; return lengte_VALUE; }
int strcmp(const char *voor_VALUE, const char *TERUG_VALUE) {
    while (*voor_VALUE && *voor_VALUE == *TERUG_VALUE) { voor_VALUE++; TERUG_VALUE++; }
    return (unsigned char)*voor_VALUE - (unsigned char)*TERUG_VALUE;
}
int memcmp(const void *voor_VALUE, const void *TERUG_VALUE, size_t greep_COUNT) {
    const unsigned char *가 = voor_VALUE, *나 = TERUG_VALUE;
    for (size_t gleuf_inskrywing = 0; gleuf_inskrywing < greep_COUNT; gleuf_inskrywing++) if (가[gleuf_inskrywing] != 나[gleuf_inskrywing]) return 가[gleuf_inskrywing] - 나[gleuf_inskrywing];
    return 0;
}
void *memcpy(void *bestemming_VALUE, const void *원본, size_t greep_COUNT) {
    unsigned char *가 = bestemming_VALUE; const unsigned char *나 = 원본;
    for (size_t gleuf_inskrywing = 0; gleuf_inskrywing < greep_COUNT; gleuf_inskrywing++) 가[gleuf_inskrywing] = 나[gleuf_inskrywing];
    return bestemming_VALUE;
}
void *memset(void *bestemming_VALUE, int VALUE, size_t greep_COUNT) {
    unsigned char *data = bestemming_VALUE;
    for (size_t gleuf_inskrywing = 0; gleuf_inskrywing < greep_COUNT; gleuf_inskrywing++) data[gleuf_inskrywing] = VALUE;
    return bestemming_VALUE;
}
int putchar(int 문자) { unsigned char VALUE = 문자; return write(1, &VALUE, 1) == 1 ? VALUE : EOF; }
int puts(const char *string_VALUE) {
    size_t lengte_VALUE = strlen(string_VALUE), Posisie = 0;
    while (Posisie < lengte_VALUE) { ssize_t maatreël = write(1, string_VALUE + Posisie, lengte_VALUE - Posisie); if (maatreël <= 0) return EOF; Posisie += maatreël; }
    return putchar('\n') == EOF ? EOF : 0;
}
