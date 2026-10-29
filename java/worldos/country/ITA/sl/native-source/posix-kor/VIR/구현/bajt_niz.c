#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *niz_VALUE) { size_t 길이 = 0; while (niz_VALUE[길이]) 길이++; return 길이; }
int strcmp(const char *sprednja_VALUE, const char *ZAJ_VALUE) {
    while (*sprednja_VALUE && *sprednja_VALUE == *ZAJ_VALUE) { sprednja_VALUE++; ZAJ_VALUE++; }
    return (unsigned char)*sprednja_VALUE - (unsigned char)*ZAJ_VALUE;
}
int memcmp(const void *sprednja_VALUE, const void *ZAJ_VALUE, size_t bajt_COUNT) {
    const unsigned char *가 = sprednja_VALUE, *SECOND_operand = ZAJ_VALUE;
    for (size_t 칸 = 0; 칸 < bajt_COUNT; 칸++) if (가[칸] != SECOND_operand[칸]) return 가[칸] - SECOND_operand[칸];
    return 0;
}
void *memcpy(void *cilj_VALUE, const void *원본, size_t bajt_COUNT) {
    unsigned char *가 = cilj_VALUE; const unsigned char *SECOND_operand = 원본;
    for (size_t 칸 = 0; 칸 < bajt_COUNT; 칸++) 가[칸] = SECOND_operand[칸];
    return cilj_VALUE;
}
void *memset(void *cilj_VALUE, int VALUE, size_t bajt_COUNT) {
    unsigned char *podatki = cilj_VALUE;
    for (size_t 칸 = 0; 칸 < bajt_COUNT; 칸++) podatki[칸] = VALUE;
    return cilj_VALUE;
}
int putchar(int 문자) { unsigned char VALUE = 문자; return write(1, &VALUE, 1) == 1 ? VALUE : EOF; }
int puts(const char *niz_VALUE) {
    size_t 길이 = strlen(niz_VALUE), Položaj = 0;
    while (Položaj < 길이) { ssize_t REZULTAT = write(1, niz_VALUE + Položaj, 길이 - Položaj); if (REZULTAT <= 0) return EOF; Položaj += REZULTAT; }
    return putchar('\n') == EOF ? EOF : 0;
}
