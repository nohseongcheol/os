#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *qimiaq_atuutilik) { size_t takininga_atuutilik = 0; while (qimiaq_atuutilik[takininga_atuutilik]) takininga_atuutilik++; return takininga_atuutilik; }
int strcmp(const char *앞, const char *Utimut_atuutilik) {
    while (*앞 && *앞 == *Utimut_atuutilik) { 앞++; Utimut_atuutilik++; }
    return (unsigned char)*앞 - (unsigned char)*Utimut_atuutilik;
}
int memcmp(const void *앞, const void *Utimut_atuutilik, size_t 바이트수) {
    const unsigned char *가 = 앞, *나 = Utimut_atuutilik;
    for (size_t 칸 = 0; 칸 < 바이트수; 칸++) if (가[칸] != 나[칸]) return 가[칸] - 나[칸];
    return 0;
}
void *memcpy(void *namunngarvik_atuutilik, const void *원본, size_t 바이트수) {
    unsigned char *가 = namunngarvik_atuutilik; const unsigned char *나 = 원본;
    for (size_t 칸 = 0; 칸 < 바이트수; 칸++) 가[칸] = 나[칸];
    return namunngarvik_atuutilik;
}
void *memset(void *namunngarvik_atuutilik, int atuutilik, size_t 바이트수) {
    unsigned char *titiqqat = namunngarvik_atuutilik;
    for (size_t 칸 = 0; 칸 < 바이트수; 칸++) titiqqat[칸] = atuutilik;
    return namunngarvik_atuutilik;
}
int putchar(int 문자) { unsigned char atuutilik = 문자; return write(1, &atuutilik, 1) == 1 ? atuutilik : EOF; }
int puts(const char *qimiaq_atuutilik) {
    size_t takininga_atuutilik = strlen(qimiaq_atuutilik), 위치 = 0;
    while (위치 < takininga_atuutilik) { ssize_t 결과 = write(1, qimiaq_atuutilik + 위치, takininga_atuutilik - 위치); if (결과 <= 0) return EOF; 위치 += 결과; }
    return putchar('\n') == EOF ? EOF : 0;
}
