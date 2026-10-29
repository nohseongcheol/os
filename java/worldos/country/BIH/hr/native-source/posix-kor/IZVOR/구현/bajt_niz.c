#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *niz_VALUE) { size_t 길이 = 0; while (niz_VALUE[길이]) 길이++; return 길이; }
int strcmp(const char *prednja_VALUE, const char *TRAG_VALUE) {
    while (*prednja_VALUE && *prednja_VALUE == *TRAG_VALUE) { prednja_VALUE++; TRAG_VALUE++; }
    return (unsigned char)*prednja_VALUE - (unsigned char)*TRAG_VALUE;
}
int memcmp(const void *prednja_VALUE, const void *TRAG_VALUE, size_t bajt_COUNT) {
    const unsigned char *가 = prednja_VALUE, *SECOND_operand = TRAG_VALUE;
    for (size_t 칸 = 0; 칸 < bajt_COUNT; 칸++) if (가[칸] != SECOND_operand[칸]) return 가[칸] - SECOND_operand[칸];
    return 0;
}
void *memcpy(void *odredište_VALUE, const void *원본, size_t bajt_COUNT) {
    unsigned char *가 = odredište_VALUE; const unsigned char *SECOND_operand = 원본;
    for (size_t 칸 = 0; 칸 < bajt_COUNT; 칸++) 가[칸] = SECOND_operand[칸];
    return odredište_VALUE;
}
void *memset(void *odredište_VALUE, int VALUE, size_t bajt_COUNT) {
    unsigned char *podaci = odredište_VALUE;
    for (size_t 칸 = 0; 칸 < bajt_COUNT; 칸++) podaci[칸] = VALUE;
    return odredište_VALUE;
}
int putchar(int 문자) { unsigned char VALUE = 문자; return write(1, &VALUE, 1) == 1 ? VALUE : EOF; }
int puts(const char *niz_VALUE) {
    size_t 길이 = strlen(niz_VALUE), Položaj = 0;
    while (Položaj < 길이) { ssize_t REZULTAT = write(1, niz_VALUE + Položaj, 길이 - Položaj); if (REZULTAT <= 0) return EOF; Položaj += REZULTAT; }
    return putchar('\n') == EOF ? EOF : 0;
}
