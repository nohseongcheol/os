#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *streng_VALUE) { size_t lengd_VALUE = 0; while (streng_VALUE[lengd_VALUE]) lengd_VALUE++; return lengd_VALUE; }
int strcmp(const char *앞, const char *TILBAKE_VALUE) {
    while (*앞 && *앞 == *TILBAKE_VALUE) { 앞++; TILBAKE_VALUE++; }
    return (unsigned char)*앞 - (unsigned char)*TILBAKE_VALUE;
}
int memcmp(const void *앞, const void *TILBAKE_VALUE, size_t byte_COUNT) {
    const unsigned char *가 = 앞, *나 = TILBAKE_VALUE;
    for (size_t felt_oppføring = 0; felt_oppføring < byte_COUNT; felt_oppføring++) if (가[felt_oppføring] != 나[felt_oppføring]) return 가[felt_oppføring] - 나[felt_oppføring];
    return 0;
}
void *memcpy(void *mål_VALUE, const void *원본, size_t byte_COUNT) {
    unsigned char *가 = mål_VALUE; const unsigned char *나 = 원본;
    for (size_t felt_oppføring = 0; felt_oppføring < byte_COUNT; felt_oppføring++) 가[felt_oppføring] = 나[felt_oppføring];
    return mål_VALUE;
}
void *memset(void *mål_VALUE, int VALUE, size_t byte_COUNT) {
    unsigned char *data = mål_VALUE;
    for (size_t felt_oppføring = 0; felt_oppføring < byte_COUNT; felt_oppføring++) data[felt_oppføring] = VALUE;
    return mål_VALUE;
}
int putchar(int 문자) { unsigned char VALUE = 문자; return write(1, &VALUE, 1) == 1 ? VALUE : EOF; }
int puts(const char *streng_VALUE) {
    size_t lengd_VALUE = strlen(streng_VALUE), Posisjon = 0;
    while (Posisjon < lengd_VALUE) { ssize_t forretningsmål = write(1, streng_VALUE + Posisjon, lengd_VALUE - Posisjon); if (forretningsmål <= 0) return EOF; Posisjon += forretningsmål; }
    return putchar('\n') == EOF ? EOF : 0;
}
