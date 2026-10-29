#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *niska_VALUE) { size_t 길이 = 0; while (niska_VALUE[길이]) 길이++; return 길이; }
int strcmp(const char *čeona_kamera_VALUE, const char *NAZAD_VALUE) {
    while (*čeona_kamera_VALUE && *čeona_kamera_VALUE == *NAZAD_VALUE) { čeona_kamera_VALUE++; NAZAD_VALUE++; }
    return (unsigned char)*čeona_kamera_VALUE - (unsigned char)*NAZAD_VALUE;
}
int memcmp(const void *čeona_kamera_VALUE, const void *NAZAD_VALUE, size_t bajt_COUNT) {
    const unsigned char *가 = čeona_kamera_VALUE, *SECOND_operand = NAZAD_VALUE;
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
int puts(const char *niska_VALUE) {
    size_t 길이 = strlen(niska_VALUE), pozicija = 0;
    while (pozicija < 길이) { ssize_t KR = write(1, niska_VALUE + pozicija, 길이 - pozicija); if (KR <= 0) return EOF; pozicija += KR; }
    return putchar('\n') == EOF ? EOF : 0;
}
