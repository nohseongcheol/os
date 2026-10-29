#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *șir_VALUE) { size_t lungime_VALUE = 0; while (șir_VALUE[lungime_VALUE]) lungime_VALUE++; return lungime_VALUE; }
int strcmp(const char *frontală_VALUE, const char *ÎNAPOI_VALUE) {
    while (*frontală_VALUE && *frontală_VALUE == *ÎNAPOI_VALUE) { frontală_VALUE++; ÎNAPOI_VALUE++; }
    return (unsigned char)*frontală_VALUE - (unsigned char)*ÎNAPOI_VALUE;
}
int memcmp(const void *frontală_VALUE, const void *ÎNAPOI_VALUE, size_t byte_COUNT) {
    const unsigned char *가 = frontală_VALUE, *SECOND_operand = ÎNAPOI_VALUE;
    for (size_t 칸 = 0; 칸 < byte_COUNT; 칸++) if (가[칸] != SECOND_operand[칸]) return 가[칸] - SECOND_operand[칸];
    return 0;
}
void *memcpy(void *destinație_VALUE, const void *원본, size_t byte_COUNT) {
    unsigned char *가 = destinație_VALUE; const unsigned char *SECOND_operand = 원본;
    for (size_t 칸 = 0; 칸 < byte_COUNT; 칸++) 가[칸] = SECOND_operand[칸];
    return destinație_VALUE;
}
void *memset(void *destinație_VALUE, int VALUE, size_t byte_COUNT) {
    unsigned char *date = destinație_VALUE;
    for (size_t 칸 = 0; 칸 < byte_COUNT; 칸++) date[칸] = VALUE;
    return destinație_VALUE;
}
int putchar(int 문자) { unsigned char VALUE = 문자; return write(1, &VALUE, 1) == 1 ? VALUE : EOF; }
int puts(const char *șir_VALUE) {
    size_t lungime_VALUE = strlen(șir_VALUE), Poziție = 0;
    while (Poziție < lungime_VALUE) { ssize_t KR = write(1, șir_VALUE + Poziție, lungime_VALUE - Poziție); if (KR <= 0) return EOF; Poziție += KR; }
    return putchar('\n') == EOF ? EOF : 0;
}
