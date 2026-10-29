#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *uchunge_inani) { size_t ubude_inani = 0; while (uchunge_inani[ubude_inani]) ubude_inani++; return ubude_inani; }
int strcmp(const char *앞, const char *Impindamuva_inani) {
    while (*앞 && *앞 == *Impindamuva_inani) { 앞++; Impindamuva_inani++; }
    return (unsigned char)*앞 - (unsigned char)*Impindamuva_inani;
}
int memcmp(const void *앞, const void *Impindamuva_inani, size_t 바이트수) {
    const unsigned char *가 = 앞, *나 = Impindamuva_inani;
    for (size_t isikhala_okufakwayo = 0; isikhala_okufakwayo < 바이트수; isikhala_okufakwayo++) if (가[isikhala_okufakwayo] != 나[isikhala_okufakwayo]) return 가[isikhala_okufakwayo] - 나[isikhala_okufakwayo];
    return 0;
}
void *memcpy(void *isikhumulo_inani, const void *원본, size_t 바이트수) {
    unsigned char *가 = isikhumulo_inani; const unsigned char *나 = 원본;
    for (size_t isikhala_okufakwayo = 0; isikhala_okufakwayo < 바이트수; isikhala_okufakwayo++) 가[isikhala_okufakwayo] = 나[isikhala_okufakwayo];
    return isikhumulo_inani;
}
void *memset(void *isikhumulo_inani, int inani, size_t 바이트수) {
    unsigned char *imininingwane = isikhumulo_inani;
    for (size_t isikhala_okufakwayo = 0; isikhala_okufakwayo < 바이트수; isikhala_okufakwayo++) imininingwane[isikhala_okufakwayo] = inani;
    return isikhumulo_inani;
}
int putchar(int 문자) { unsigned char inani = 문자; return write(1, &inani, 1) == 1 ? inani : EOF; }
int puts(const char *uchunge_inani) {
    size_t ubude_inani = strlen(uchunge_inani), 위치 = 0;
    while (위치 < ubude_inani) { ssize_t 결과 = write(1, uchunge_inani + 위치, ubude_inani - 위치); if (결과 <= 0) return EOF; 위치 += 결과; }
    return putchar('\n') == EOF ? EOF : 0;
}
