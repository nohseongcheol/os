#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *virkne_VALUE) { size_t 길이 = 0; while (virkne_VALUE[길이]) 길이++; return 길이; }
int strcmp(const char *priekšējā_VALUE, const char *ATPAKAĻ_VALUE) {
    while (*priekšējā_VALUE && *priekšējā_VALUE == *ATPAKAĻ_VALUE) { priekšējā_VALUE++; ATPAKAĻ_VALUE++; }
    return (unsigned char)*priekšējā_VALUE - (unsigned char)*ATPAKAĻ_VALUE;
}
int memcmp(const void *priekšējā_VALUE, const void *ATPAKAĻ_VALUE, size_t byte_COUNT) {
    const unsigned char *가 = priekšējā_VALUE, *SECOND_operands = ATPAKAĻ_VALUE;
    for (size_t 칸 = 0; 칸 < byte_COUNT; 칸++) if (가[칸] != SECOND_operands[칸]) return 가[칸] - SECOND_operands[칸];
    return 0;
}
void *memcpy(void *mērķis_VALUE, const void *원본, size_t byte_COUNT) {
    unsigned char *가 = mērķis_VALUE; const unsigned char *SECOND_operands = 원본;
    for (size_t 칸 = 0; 칸 < byte_COUNT; 칸++) 가[칸] = SECOND_operands[칸];
    return mērķis_VALUE;
}
void *memset(void *mērķis_VALUE, int VALUE, size_t byte_COUNT) {
    unsigned char *dati = mērķis_VALUE;
    for (size_t 칸 = 0; 칸 < byte_COUNT; 칸++) dati[칸] = VALUE;
    return mērķis_VALUE;
}
int putchar(int 문자) { unsigned char VALUE = 문자; return write(1, &VALUE, 1) == 1 ? VALUE : EOF; }
int puts(const char *virkne_VALUE) {
    size_t 길이 = strlen(virkne_VALUE), Novietojums = 0;
    while (Novietojums < 길이) { ssize_t mērs = write(1, virkne_VALUE + Novietojums, 길이 - Novietojums); if (mērs <= 0) return EOF; Novietojums += mērs; }
    return putchar('\n') == EOF ? EOF : 0;
}
