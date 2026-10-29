#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *dikwalwa_Boleng) { size_t boleele_Boleng = 0; while (dikwalwa_Boleng[boleele_Boleng]) boleele_Boleng++; return boleele_Boleng; }
int strcmp(const char *앞, const char *Morago_Boleng) {
    while (*앞 && *앞 == *Morago_Boleng) { 앞++; Morago_Boleng++; }
    return (unsigned char)*앞 - (unsigned char)*Morago_Boleng;
}
int memcmp(const void *앞, const void *Morago_Boleng, size_t 바이트수) {
    const unsigned char *가 = 앞, *나 = Morago_Boleng;
    for (size_t sebaka_tsenyo = 0; sebaka_tsenyo < 바이트수; sebaka_tsenyo++) if (가[sebaka_tsenyo] != 나[sebaka_tsenyo]) return 가[sebaka_tsenyo] - 나[sebaka_tsenyo];
    return 0;
}
void *memcpy(void *bogorogelo_Boleng, const void *원본, size_t 바이트수) {
    unsigned char *가 = bogorogelo_Boleng; const unsigned char *나 = 원본;
    for (size_t sebaka_tsenyo = 0; sebaka_tsenyo < 바이트수; sebaka_tsenyo++) 가[sebaka_tsenyo] = 나[sebaka_tsenyo];
    return bogorogelo_Boleng;
}
void *memset(void *bogorogelo_Boleng, int Boleng, size_t 바이트수) {
    unsigned char *tshedimosetso = bogorogelo_Boleng;
    for (size_t sebaka_tsenyo = 0; sebaka_tsenyo < 바이트수; sebaka_tsenyo++) tshedimosetso[sebaka_tsenyo] = Boleng;
    return bogorogelo_Boleng;
}
int putchar(int 문자) { unsigned char Boleng = 문자; return write(1, &Boleng, 1) == 1 ? Boleng : EOF; }
int puts(const char *dikwalwa_Boleng) {
    size_t boleele_Boleng = strlen(dikwalwa_Boleng), 위치 = 0;
    while (위치 < boleele_Boleng) { ssize_t 결과 = write(1, dikwalwa_Boleng + 위치, boleele_Boleng - 위치); if (결과 <= 0) return EOF; 위치 += 결과; }
    return putchar('\n') == EOF ? EOF : 0;
}
