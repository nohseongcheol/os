#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *string_VALUE) { size_t 길이 = 0; while (string_VALUE[길이]) 길이++; return 길이; }
int strcmp(const char *esikaamera_VALUE, const char *Tagasi_VALUE) {
    while (*esikaamera_VALUE && *esikaamera_VALUE == *Tagasi_VALUE) { esikaamera_VALUE++; Tagasi_VALUE++; }
    return (unsigned char)*esikaamera_VALUE - (unsigned char)*Tagasi_VALUE;
}
int memcmp(const void *esikaamera_VALUE, const void *Tagasi_VALUE, size_t bait_COUNT) {
    const unsigned char *가 = esikaamera_VALUE, *SECOND_operand = Tagasi_VALUE;
    for (size_t 칸 = 0; 칸 < bait_COUNT; 칸++) if (가[칸] != SECOND_operand[칸]) return 가[칸] - SECOND_operand[칸];
    return 0;
}
void *memcpy(void *sihtkoht_VALUE, const void *원본, size_t bait_COUNT) {
    unsigned char *가 = sihtkoht_VALUE; const unsigned char *SECOND_operand = 원본;
    for (size_t 칸 = 0; 칸 < bait_COUNT; 칸++) 가[칸] = SECOND_operand[칸];
    return sihtkoht_VALUE;
}
void *memset(void *sihtkoht_VALUE, int VALUE, size_t bait_COUNT) {
    unsigned char *andmed = sihtkoht_VALUE;
    for (size_t 칸 = 0; 칸 < bait_COUNT; 칸++) andmed[칸] = VALUE;
    return sihtkoht_VALUE;
}
int putchar(int 문자) { unsigned char VALUE = 문자; return write(1, &VALUE, 1) == 1 ? VALUE : EOF; }
int puts(const char *string_VALUE) {
    size_t 길이 = strlen(string_VALUE), Asukoht = 0;
    while (Asukoht < 길이) { ssize_t TULEMUS = write(1, string_VALUE + Asukoht, 길이 - Asukoht); if (TULEMUS <= 0) return EOF; Asukoht += TULEMUS; }
    return putchar('\n') == EOF ? EOF : 0;
}
