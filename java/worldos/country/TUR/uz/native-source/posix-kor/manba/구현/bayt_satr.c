#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *satr_VALUE) { size_t uzunlik_VALUE = 0; while (satr_VALUE[uzunlik_VALUE]) uzunlik_VALUE++; return uzunlik_VALUE; }
int strcmp(const char *old_kamera_VALUE, const char *Orqaga_VALUE) {
    while (*old_kamera_VALUE && *old_kamera_VALUE == *Orqaga_VALUE) { old_kamera_VALUE++; Orqaga_VALUE++; }
    return (unsigned char)*old_kamera_VALUE - (unsigned char)*Orqaga_VALUE;
}
int memcmp(const void *old_kamera_VALUE, const void *Orqaga_VALUE, size_t bayt_COUNT) {
    const unsigned char *가 = old_kamera_VALUE, *나 = Orqaga_VALUE;
    for (size_t in_kiritish = 0; in_kiritish < bayt_COUNT; in_kiritish++) if (가[in_kiritish] != 나[in_kiritish]) return 가[in_kiritish] - 나[in_kiritish];
    return 0;
}
void *memcpy(void *ko_chirish_joyi_VALUE, const void *원본, size_t bayt_COUNT) {
    unsigned char *가 = ko_chirish_joyi_VALUE; const unsigned char *나 = 원본;
    for (size_t in_kiritish = 0; in_kiritish < bayt_COUNT; in_kiritish++) 가[in_kiritish] = 나[in_kiritish];
    return ko_chirish_joyi_VALUE;
}
void *memset(void *ko_chirish_joyi_VALUE, int VALUE, size_t bayt_COUNT) {
    unsigned char *ma_lumotlar = ko_chirish_joyi_VALUE;
    for (size_t in_kiritish = 0; in_kiritish < bayt_COUNT; in_kiritish++) ma_lumotlar[in_kiritish] = VALUE;
    return ko_chirish_joyi_VALUE;
}
int putchar(int 문자) { unsigned char VALUE = 문자; return write(1, &VALUE, 1) == 1 ? VALUE : EOF; }
int puts(const char *satr_VALUE) {
    size_t uzunlik_VALUE = strlen(satr_VALUE), Holati = 0;
    while (Holati < uzunlik_VALUE) { ssize_t o_lchov = write(1, satr_VALUE + Holati, uzunlik_VALUE - Holati); if (o_lchov <= 0) return EOF; Holati += o_lchov; }
    return putchar('\n') == EOF ? EOF : 0;
}
