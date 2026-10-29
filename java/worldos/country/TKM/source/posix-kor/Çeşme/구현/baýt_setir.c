#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *setir_baha_6ca8363c) { size_t dowamlylyk_baha = 0; while (setir_baha_6ca8363c[dowamlylyk_baha]) dowamlylyk_baha++; return dowamlylyk_baha; }
int strcmp(const char *앞, const char *Yza_baha) {
    while (*앞 && *앞 == *Yza_baha) { 앞++; Yza_baha++; }
    return (unsigned char)*앞 - (unsigned char)*Yza_baha;
}
int memcmp(const void *앞, const void *Yza_baha, size_t 바이트수) {
    const unsigned char *가 = 앞, *나 = Yza_baha;
    for (size_t ýer_girizmeklik = 0; ýer_girizmeklik < 바이트수; ýer_girizmeklik++) if (가[ýer_girizmeklik] != 나[ýer_girizmeklik]) return 가[ýer_girizmeklik] - 나[ýer_girizmeklik];
    return 0;
}
void *memcpy(void *barylmaly_ýer_baha, const void *원본, size_t 바이트수) {
    unsigned char *가 = barylmaly_ýer_baha; const unsigned char *나 = 원본;
    for (size_t ýer_girizmeklik = 0; ýer_girizmeklik < 바이트수; ýer_girizmeklik++) 가[ýer_girizmeklik] = 나[ýer_girizmeklik];
    return barylmaly_ýer_baha;
}
void *memset(void *barylmaly_ýer_baha, int baha, size_t 바이트수) {
    unsigned char *maglumat = barylmaly_ýer_baha;
    for (size_t ýer_girizmeklik = 0; ýer_girizmeklik < 바이트수; ýer_girizmeklik++) maglumat[ýer_girizmeklik] = baha;
    return barylmaly_ýer_baha;
}
int putchar(int 문자) { unsigned char baha = 문자; return write(1, &baha, 1) == 1 ? baha : EOF; }
int puts(const char *setir_baha_6ca8363c) {
    size_t dowamlylyk_baha = strlen(setir_baha_6ca8363c), 위치 = 0;
    while (위치 < dowamlylyk_baha) { ssize_t 결과 = write(1, setir_baha_6ca8363c + 위치, dowamlylyk_baha - 위치); if (결과 <= 0) return EOF; 위치 += 결과; }
    return putchar('\n') == EOF ? EOF : 0;
}
