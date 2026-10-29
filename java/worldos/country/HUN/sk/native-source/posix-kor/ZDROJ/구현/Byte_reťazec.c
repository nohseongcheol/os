#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *reťazec_VALUE) { size_t dĺžka_VALUE = 0; while (reťazec_VALUE[dĺžka_VALUE]) dĺžka_VALUE++; return dĺžka_VALUE; }
int strcmp(const char *predný_VALUE, const char *BACK_VALUE) {
    while (*predný_VALUE && *predný_VALUE == *BACK_VALUE) { predný_VALUE++; BACK_VALUE++; }
    return (unsigned char)*predný_VALUE - (unsigned char)*BACK_VALUE;
}
int memcmp(const void *predný_VALUE, const void *BACK_VALUE, size_t Byte_COUNT) {
    const unsigned char *가 = predný_VALUE, *SECOND_operand = BACK_VALUE;
    for (size_t 칸 = 0; 칸 < Byte_COUNT; 칸++) if (가[칸] != SECOND_operand[칸]) return 가[칸] - SECOND_operand[칸];
    return 0;
}
void *memcpy(void *cieľ_VALUE, const void *원본, size_t Byte_COUNT) {
    unsigned char *가 = cieľ_VALUE; const unsigned char *SECOND_operand = 원본;
    for (size_t 칸 = 0; 칸 < Byte_COUNT; 칸++) 가[칸] = SECOND_operand[칸];
    return cieľ_VALUE;
}
void *memset(void *cieľ_VALUE, int VALUE, size_t Byte_COUNT) {
    unsigned char *údaje = cieľ_VALUE;
    for (size_t 칸 = 0; 칸 < Byte_COUNT; 칸++) údaje[칸] = VALUE;
    return cieľ_VALUE;
}
int putchar(int 문자) { unsigned char VALUE = 문자; return write(1, &VALUE, 1) == 1 ? VALUE : EOF; }
int puts(const char *reťazec_VALUE) {
    size_t dĺžka_VALUE = strlen(reťazec_VALUE), Pozícia = 0;
    while (Pozícia < dĺžka_VALUE) { ssize_t KR = write(1, reťazec_VALUE + Pozícia, dĺžka_VALUE - Pozícia); if (KR <= 0) return EOF; Pozícia += KR; }
    return putchar('\n') == EOF ? EOF : 0;
}
