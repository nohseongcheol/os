#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *eilutė_VALUE) { size_t 길이 = 0; while (eilutė_VALUE[길이]) 길이++; return 길이; }
int strcmp(const char *priekinis_VALUE, const char *ATGAL_VALUE) {
    while (*priekinis_VALUE && *priekinis_VALUE == *ATGAL_VALUE) { priekinis_VALUE++; ATGAL_VALUE++; }
    return (unsigned char)*priekinis_VALUE - (unsigned char)*ATGAL_VALUE;
}
int memcmp(const void *priekinis_VALUE, const void *ATGAL_VALUE, size_t baitas_COUNT) {
    const unsigned char *가 = priekinis_VALUE, *SECOND_operandas = ATGAL_VALUE;
    for (size_t 칸 = 0; 칸 < baitas_COUNT; 칸++) if (가[칸] != SECOND_operandas[칸]) return 가[칸] - SECOND_operandas[칸];
    return 0;
}
void *memcpy(void *vieta_VALUE, const void *원본, size_t baitas_COUNT) {
    unsigned char *가 = vieta_VALUE; const unsigned char *SECOND_operandas = 원본;
    for (size_t 칸 = 0; 칸 < baitas_COUNT; 칸++) 가[칸] = SECOND_operandas[칸];
    return vieta_VALUE;
}
void *memset(void *vieta_VALUE, int VALUE, size_t baitas_COUNT) {
    unsigned char *duomenys = vieta_VALUE;
    for (size_t 칸 = 0; 칸 < baitas_COUNT; 칸++) duomenys[칸] = VALUE;
    return vieta_VALUE;
}
int putchar(int 문자) { unsigned char VALUE = 문자; return write(1, &VALUE, 1) == 1 ? VALUE : EOF; }
int puts(const char *eilutė_VALUE) {
    size_t 길이 = strlen(eilutė_VALUE), Pozicija = 0;
    while (Pozicija < 길이) { ssize_t REZULTATAS = write(1, eilutė_VALUE + Pozicija, 길이 - Pozicija); if (REZULTATAS <= 0) return EOF; Pozicija += REZULTATAS; }
    return putchar('\n') == EOF ? EOF : 0;
}
