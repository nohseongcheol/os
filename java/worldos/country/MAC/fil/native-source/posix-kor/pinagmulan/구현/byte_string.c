#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *string_VALUE) { size_t haba_VALUE = 0; while (string_VALUE[haba_VALUE]) haba_VALUE++; return haba_VALUE; }
int strcmp(const char *nasa_harap_VALUE, const char *Bumalik_VALUE) {
    while (*nasa_harap_VALUE && *nasa_harap_VALUE == *Bumalik_VALUE) { nasa_harap_VALUE++; Bumalik_VALUE++; }
    return (unsigned char)*nasa_harap_VALUE - (unsigned char)*Bumalik_VALUE;
}
int memcmp(const void *nasa_harap_VALUE, const void *Bumalik_VALUE, size_t byte_COUNT) {
    const unsigned char *가 = nasa_harap_VALUE, *나 = Bumalik_VALUE;
    for (size_t espasyo_pagpasok = 0; espasyo_pagpasok < byte_COUNT; espasyo_pagpasok++) if (가[espasyo_pagpasok] != 나[espasyo_pagpasok]) return 가[espasyo_pagpasok] - 나[espasyo_pagpasok];
    return 0;
}
void *memcpy(void *patutunguhan_VALUE, const void *원본, size_t byte_COUNT) {
    unsigned char *가 = patutunguhan_VALUE; const unsigned char *나 = 원본;
    for (size_t espasyo_pagpasok = 0; espasyo_pagpasok < byte_COUNT; espasyo_pagpasok++) 가[espasyo_pagpasok] = 나[espasyo_pagpasok];
    return patutunguhan_VALUE;
}
void *memset(void *patutunguhan_VALUE, int VALUE, size_t byte_COUNT) {
    unsigned char *data = patutunguhan_VALUE;
    for (size_t espasyo_pagpasok = 0; espasyo_pagpasok < byte_COUNT; espasyo_pagpasok++) data[espasyo_pagpasok] = VALUE;
    return patutunguhan_VALUE;
}
int putchar(int 문자) { unsigned char VALUE = 문자; return write(1, &VALUE, 1) == 1 ? VALUE : EOF; }
int puts(const char *string_VALUE) {
    size_t haba_VALUE = strlen(string_VALUE), posisyon = 0;
    while (posisyon < haba_VALUE) { ssize_t sukat = write(1, string_VALUE + posisyon, haba_VALUE - posisyon); if (sukat <= 0) return EOF; posisyon += sukat; }
    return putchar('\n') == EOF ? EOF : 0;
}
