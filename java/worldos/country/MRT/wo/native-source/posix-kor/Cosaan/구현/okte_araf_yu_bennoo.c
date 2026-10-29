#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *araf_yu_bennoo_xëyma) { size_t diir_xëyma = 0; while (araf_yu_bennoo_xëyma[diir_xëyma]) diir_xëyma++; return diir_xëyma; }
int strcmp(const char *앞, const char *woñeeku_xëyma) {
    while (*앞 && *앞 == *woñeeku_xëyma) { 앞++; woñeeku_xëyma++; }
    return (unsigned char)*앞 - (unsigned char)*woñeeku_xëyma;
}
int memcmp(const void *앞, const void *woñeeku_xëyma, size_t 바이트수) {
    const unsigned char *가 = 앞, *나 = woñeeku_xëyma;
    for (size_t xar_xar_dugal_xabaar = 0; xar_xar_dugal_xabaar < 바이트수; xar_xar_dugal_xabaar++) if (가[xar_xar_dugal_xabaar] != 나[xar_xar_dugal_xabaar]) return 가[xar_xar_dugal_xabaar] - 나[xar_xar_dugal_xabaar];
    return 0;
}
void *memcpy(void *jëmmukaay_xëyma, const void *원본, size_t 바이트수) {
    unsigned char *가 = jëmmukaay_xëyma; const unsigned char *나 = 원본;
    for (size_t xar_xar_dugal_xabaar = 0; xar_xar_dugal_xabaar < 바이트수; xar_xar_dugal_xabaar++) 가[xar_xar_dugal_xabaar] = 나[xar_xar_dugal_xabaar];
    return jëmmukaay_xëyma;
}
void *memset(void *jëmmukaay_xëyma, int xëyma, size_t 바이트수) {
    unsigned char *mbir = jëmmukaay_xëyma;
    for (size_t xar_xar_dugal_xabaar = 0; xar_xar_dugal_xabaar < 바이트수; xar_xar_dugal_xabaar++) mbir[xar_xar_dugal_xabaar] = xëyma;
    return jëmmukaay_xëyma;
}
int putchar(int 문자) { unsigned char xëyma = 문자; return write(1, &xëyma, 1) == 1 ? xëyma : EOF; }
int puts(const char *araf_yu_bennoo_xëyma) {
    size_t diir_xëyma = strlen(araf_yu_bennoo_xëyma), 위치 = 0;
    while (위치 < diir_xëyma) { ssize_t 결과 = write(1, araf_yu_bennoo_xëyma + 위치, diir_xëyma - 위치); if (결과 <= 0) return EOF; 위치 += 결과; }
    return putchar('\n') == EOF ? EOF : 0;
}
