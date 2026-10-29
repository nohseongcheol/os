#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *aho_uara) { size_t roa_uara = 0; while (aho_uara[roa_uara]) roa_uara++; return roa_uara; }
int strcmp(const char *앞, const char *Hoki_uara) {
    while (*앞 && *앞 == *Hoki_uara) { 앞++; Hoki_uara++; }
    return (unsigned char)*앞 - (unsigned char)*Hoki_uara;
}
int memcmp(const void *앞, const void *Hoki_uara, size_t paita_COUNT) {
    const unsigned char *가 = 앞, *나 = Hoki_uara;
    for (size_t kāniwha_tāurunga = 0; kāniwha_tāurunga < paita_COUNT; kāniwha_tāurunga++) if (가[kāniwha_tāurunga] != 나[kāniwha_tāurunga]) return 가[kāniwha_tāurunga] - 나[kāniwha_tāurunga];
    return 0;
}
void *memcpy(void *ūnga_uara, const void *원본, size_t paita_COUNT) {
    unsigned char *가 = ūnga_uara; const unsigned char *나 = 원본;
    for (size_t kāniwha_tāurunga = 0; kāniwha_tāurunga < paita_COUNT; kāniwha_tāurunga++) 가[kāniwha_tāurunga] = 나[kāniwha_tāurunga];
    return ūnga_uara;
}
void *memset(void *ūnga_uara, int uara, size_t paita_COUNT) {
    unsigned char *raraunga = ūnga_uara;
    for (size_t kāniwha_tāurunga = 0; kāniwha_tāurunga < paita_COUNT; kāniwha_tāurunga++) raraunga[kāniwha_tāurunga] = uara;
    return ūnga_uara;
}
int putchar(int 문자) { unsigned char uara = 문자; return write(1, &uara, 1) == 1 ? uara : EOF; }
int puts(const char *aho_uara) {
    size_t roa_uara = strlen(aho_uara), tūranga = 0;
    while (tūranga < roa_uara) { ssize_t mēhua = write(1, aho_uara + tūranga, roa_uara - tūranga); if (mēhua <= 0) return EOF; tūranga += mēhua; }
    return putchar('\n') == EOF ? EOF : 0;
}
