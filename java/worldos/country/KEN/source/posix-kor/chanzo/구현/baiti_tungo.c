#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *tungo_thamani) { size_t urefu_thamani = 0; while (tungo_thamani[urefu_thamani]) urefu_thamani++; return urefu_thamani; }
int strcmp(const char *mbele_thamani, const char *Nyuma_thamani) {
    while (*mbele_thamani && *mbele_thamani == *Nyuma_thamani) { mbele_thamani++; Nyuma_thamani++; }
    return (unsigned char)*mbele_thamani - (unsigned char)*Nyuma_thamani;
}
int memcmp(const void *mbele_thamani, const void *Nyuma_thamani, size_t 바이트수) {
    const unsigned char *가 = mbele_thamani, *나 = Nyuma_thamani;
    for (size_t Sloti_ingizo = 0; Sloti_ingizo < 바이트수; Sloti_ingizo++) if (가[Sloti_ingizo] != 나[Sloti_ingizo]) return 가[Sloti_ingizo] - 나[Sloti_ingizo];
    return 0;
}
void *memcpy(void *fikio_thamani, const void *원본, size_t 바이트수) {
    unsigned char *가 = fikio_thamani; const unsigned char *나 = 원본;
    for (size_t Sloti_ingizo = 0; Sloti_ingizo < 바이트수; Sloti_ingizo++) 가[Sloti_ingizo] = 나[Sloti_ingizo];
    return fikio_thamani;
}
void *memset(void *fikio_thamani, int thamani, size_t 바이트수) {
    unsigned char *data = fikio_thamani;
    for (size_t Sloti_ingizo = 0; Sloti_ingizo < 바이트수; Sloti_ingizo++) data[Sloti_ingizo] = thamani;
    return fikio_thamani;
}
int putchar(int 문자) { unsigned char thamani = 문자; return write(1, &thamani, 1) == 1 ? thamani : EOF; }
int puts(const char *tungo_thamani) {
    size_t urefu_thamani = strlen(tungo_thamani), 위치 = 0;
    while (위치 < urefu_thamani) { ssize_t 결과 = write(1, tungo_thamani + 위치, urefu_thamani - 위치); if (결과 <= 0) return EOF; 위치 += 결과; }
    return putchar('\n') == EOF ? EOF : 0;
}
