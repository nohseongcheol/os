#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *string_VALUE) { size_t tul_VALUE = 0; while (string_VALUE[tul_VALUE]) tul_VALUE++; return tul_VALUE; }
int strcmp(const char *앞, const char *Lura_VALUE) {
    while (*앞 && *앞 == *Lura_VALUE) { 앞++; Lura_VALUE++; }
    return (unsigned char)*앞 - (unsigned char)*Lura_VALUE;
}
int memcmp(const void *앞, const void *Lura_VALUE, size_t byte_COUNT) {
    const unsigned char *가 = 앞, *나 = Lura_VALUE;
    for (size_t slott_entrata = 0; slott_entrata < byte_COUNT; slott_entrata++) if (가[slott_entrata] != 나[slott_entrata]) return 가[slott_entrata] - 나[slott_entrata];
    return 0;
}
void *memcpy(void *destinazzjoni_VALUE, const void *원본, size_t byte_COUNT) {
    unsigned char *가 = destinazzjoni_VALUE; const unsigned char *나 = 원본;
    for (size_t slott_entrata = 0; slott_entrata < byte_COUNT; slott_entrata++) 가[slott_entrata] = 나[slott_entrata];
    return destinazzjoni_VALUE;
}
void *memset(void *destinazzjoni_VALUE, int VALUE, size_t byte_COUNT) {
    unsigned char *data = destinazzjoni_VALUE;
    for (size_t slott_entrata = 0; slott_entrata < byte_COUNT; slott_entrata++) data[slott_entrata] = VALUE;
    return destinazzjoni_VALUE;
}
int putchar(int 문자) { unsigned char VALUE = 문자; return write(1, &VALUE, 1) == 1 ? VALUE : EOF; }
int puts(const char *string_VALUE) {
    size_t tul_VALUE = strlen(string_VALUE), pożizzjoni = 0;
    while (pożizzjoni < tul_VALUE) { ssize_t miżura = write(1, string_VALUE + pożizzjoni, tul_VALUE - pożizzjoni); if (miżura <= 0) return EOF; pożizzjoni += miżura; }
    return putchar('\n') == EOF ? EOF : 0;
}
